from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.core.constants import MAX_INTENTOS, MINUTOS_BLOQUEO
from app.modules.auth.domain.entity.intento_autenticacion import IntentoAutenticacion
from app.modules.auth.domain.interface.auth_repository import AuthRepository
from app.modules.usuario.infrastructure.repository.sql_usuario_repository import SqlUsuarioRepository
from app.modules.usuario.infrastructure.model.usuario_model import UsuarioModel


class SqlAuthRepository(AuthRepository):

    def __init__(self, db: Session):
        self.db = db
        self.usuario_repository = SqlUsuarioRepository()

    def login(self, correo):
        return self.usuario_repository.get_by_email(self.db, correo)

    def get_by_email(self, correo):
        return self.usuario_repository.get_by_email(self.db, correo)

    def register_failed_attempt(self, usuario_id):
        usuario = (
            self.db.query(UsuarioModel)
            .filter(UsuarioModel.id_usuario == usuario_id)
            .first()
        )

        if not usuario:
            return None

        usuario.intentos_fallidos = (usuario.intentos_fallidos or 0) + 1

        intento = IntentoAutenticacion(
            usuario.intentos_fallidos,
            usuario.bloqueado_hasta
        )

        if intento.debe_bloquearse():
            usuario.bloqueado_hasta = datetime.now(timezone.utc) + timedelta(minutes=MINUTOS_BLOQUEO)

        self.db.commit()
        self.db.refresh(usuario)
        return usuario

    def is_locked(self, usuario_id):
        usuario = (
            self.db.query(UsuarioModel)
            .filter(UsuarioModel.id_usuario == usuario_id)
            .first()
        )

        if not usuario:
            return False

        return IntentoAutenticacion(
            usuario.intentos_fallidos,
            usuario.bloqueado_hasta
        ).esta_bloqueado()

    def reset_failed_attempts(self, usuario_id):
        usuario = (
            self.db.query(UsuarioModel)
            .filter(UsuarioModel.id_usuario == usuario_id)
            .first()
        )

        if not usuario:
            return None

        usuario.intentos_fallidos = 0
        usuario.bloqueado_hasta = None

        self.db.commit()
        self.db.refresh(usuario)
        return usuario
