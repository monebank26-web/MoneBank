from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.core.constants import MINUTOS_BLOQUEO
from app.modules.auth.domain.entity.intento_autenticacion import IntentoAutenticacion
from app.modules.auth.domain.entity.reset_token import ResetToken
from app.modules.auth.domain.interface.auth_repository import AuthRepository
from app.modules.auth.infrastructure.model.reset_token_model import ResetTokenModel
from app.modules.usuario.domain.interface.usuario_repository import UsuarioRepository


class SqlAuthRepository(AuthRepository):

    def __init__(self, db: Session, usuario_repository: UsuarioRepository):
        self.db = db
        self.usuario_repository = usuario_repository

    def login(self, correo):
        return self.usuario_repository.get_by_email(correo)

    def register_failed_attempt(self, usuario_id):
        usuario = self.usuario_repository.get_by_id(usuario_id)

        if not usuario:
            return None

        nuevos_intentos = (usuario.intentos_fallidos or 0) + 1
        bloqueado_hasta = usuario.bloqueado_hasta

        intento = IntentoAutenticacion(
            nuevos_intentos,
            usuario.bloqueado_hasta
        )

        if intento.debe_bloquearse():
            bloqueado_hasta = datetime.now(timezone.utc) + timedelta(minutes=MINUTOS_BLOQUEO)

        return self.usuario_repository.update_auth_fields(
            usuario_id, nuevos_intentos, bloqueado_hasta
        )

    def is_locked(self, usuario_id):
        usuario = self.usuario_repository.get_by_id(usuario_id)

        if not usuario:
            return False

        return IntentoAutenticacion(
            usuario.intentos_fallidos,
            usuario.bloqueado_hasta
        ).esta_bloqueado()

    def reset_failed_attempts(self, usuario_id):
        return self.usuario_repository.update_auth_fields(usuario_id, 0, None)

    def create_recovery_token(self, usuario_id, token_hash, fecha_expiracion):
        token = ResetTokenModel(
            usuario_id=usuario_id,
            token_hash=token_hash,
            fecha_expiracion=fecha_expiracion
        )
        self.db.add(token)
        self.db.commit()
        self.db.refresh(token)
        return token

    def find_valid_token(self, token_hash):
        model = (
            self.db.query(ResetTokenModel)
            .filter(
                ResetTokenModel.token_hash == token_hash,
                ResetTokenModel.usado == False,
                ResetTokenModel.fecha_expiracion > datetime.now(timezone.utc)
            )
            .first()
        )
        if not model:
            return None
        return ResetToken(
            id=model.id,
            usuario_id=model.usuario_id,
            token_hash=model.token_hash,
            fecha_creacion=model.fecha_creacion,
            fecha_expiracion=model.fecha_expiracion,
            usado=model.usado
        )

    def invalidate_token(self, token_id):
        token = (
            self.db.query(ResetTokenModel)
            .filter(ResetTokenModel.id == token_id)
            .first()
        )
        if token:
            token.usado = True
            self.db.commit()

    def invalidate_user_tokens(self, usuario_id):
        self.db.query(ResetTokenModel).filter(
            ResetTokenModel.usuario_id == usuario_id,
            ResetTokenModel.usado == False
        ).update({"usado": True})
        self.db.commit()
