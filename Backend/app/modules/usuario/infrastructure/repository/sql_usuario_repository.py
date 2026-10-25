from sqlalchemy import func, or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.modules.usuario.domain.interface.usuario_repository import UsuarioRepository
from app.modules.usuario.domain.entity.usuario import Usuario
from app.modules.usuario.infrastructure.model.usuario_model import UsuarioModel
from app.shared.exceptions.auth_errors import EmailAlreadyExistsException


# Restricción única del correo en la tabla `usuario`.
RESTRICCION_CORREO_USUARIO = "usuario_correo_key"


def es_conflicto_de_correo(error) -> bool:
    """Indica si un IntegrityError viene de la restricción única del correo.

    Postgres deja el nombre de la restricción en ``error.orig.diag``; otros
    motores (SQLite en pruebas) solo lo exponen en el mensaje.
    """
    diagnostico = getattr(getattr(error, "orig", None), "diag", None)
    nombre = getattr(diagnostico, "constraint_name", None)

    if nombre:
        return nombre == RESTRICCION_CORREO_USUARIO

    return RESTRICCION_CORREO_USUARIO in str(getattr(error, "orig", None) or error)


class SqlUsuarioRepository(UsuarioRepository):

    def __init__(self, db: Session):
        self.db = db

    def _to_entity(self, modelo: UsuarioModel):
        if not modelo:
            return None

        return Usuario(
            id_usuario=modelo.id_usuario,
            nombres=modelo.nombres,
            apellidos=modelo.apellidos,
            correo=modelo.correo,
            contrasena=modelo.contrasena,
            estado=modelo.estado,
            id_rol=modelo.id_rol,
            id_tipo_usuario=modelo.id_tipo_usuario,
            fecha_creacion=modelo.fecha_creacion,
            motivo_bloqueo=modelo.motivo_bloqueo,
            fecha_bloqueo=modelo.fecha_bloqueo,
            intentos_fallidos=getattr(modelo, "intentos_fallidos", 0) or 0,
            bloqueado_hasta=getattr(modelo, "bloqueado_hasta", None),
        )

    def create(self, usuario_data):
        usuario = UsuarioModel(**usuario_data)
        self.db.add(usuario)
        self.db.flush()
        self.db.refresh(usuario)
        return usuario

    def exists_by_email(self, correo, excluir_id_usuario=None):
        if not correo:
            return False

        consulta = self.db.query(UsuarioModel).filter(
            func.lower(func.trim(UsuarioModel.correo)) == correo.strip().lower()
        )

        if excluir_id_usuario is not None:
            consulta = consulta.filter(
                UsuarioModel.id_usuario != excluir_id_usuario
            )

        return consulta.first() is not None

    def get_all(self):
        return self.db.query(UsuarioModel).all()

    def listar(self, filtros):
        consulta = self.db.query(UsuarioModel)

        buscar = (filtros.get("buscar") or "").strip()
        if buscar:
            patron = f"%{buscar}%"
            consulta = consulta.filter(
                or_(
                    UsuarioModel.nombres.ilike(patron),
                    UsuarioModel.apellidos.ilike(patron),
                    UsuarioModel.correo.ilike(patron),
                )
            )

        if filtros.get("estado"):
            consulta = consulta.filter(UsuarioModel.estado == filtros["estado"])

        if filtros.get("id_rol"):
            consulta = consulta.filter(UsuarioModel.id_rol == filtros["id_rol"])

        total = consulta.count()

        items = (
            consulta.order_by(UsuarioModel.id_usuario.asc())
            .offset((filtros["pagina"] - 1) * filtros["por_pagina"])
            .limit(filtros["por_pagina"])
            .all()
        )

        return [self._to_entity(item) for item in items], total

    def get_by_id(self, id_usuario):
        usuario = (
            self.db.query(UsuarioModel)
            .filter(UsuarioModel.id_usuario == id_usuario)
            .first()
        )
        return self._to_entity(usuario)

    def update(self, id_usuario, usuario_data):
        usuario = (
            self.db.query(UsuarioModel)
            .filter(UsuarioModel.id_usuario == id_usuario)
            .first()
        )

        if not usuario:
            return None

        for key, value in usuario_data.items():
            setattr(usuario, key, value)

        try:
            self.db.flush()
            self.db.refresh(usuario)
        except IntegrityError as error:
            self.db.rollback()

            if es_conflicto_de_correo(error):
                raise EmailAlreadyExistsException()

            raise

        return Usuario(
            id_usuario=usuario.id_usuario,
            nombres=usuario.nombres,
            apellidos=usuario.apellidos,
            correo=usuario.correo,
            contrasena=usuario.contrasena,
            estado=usuario.estado,
            id_rol=usuario.id_rol,
            id_tipo_usuario=usuario.id_tipo_usuario,
            fecha_creacion=usuario.fecha_creacion,
            motivo_bloqueo=usuario.motivo_bloqueo,
            fecha_bloqueo=usuario.fecha_bloqueo,
        )

    def delete(self, id_usuario):
        usuario = (
            self.db.query(UsuarioModel)
            .filter(UsuarioModel.id_usuario == id_usuario)
            .first()
        )

        if not usuario:
            return None

        self.db.delete(usuario)
        self.db.flush()

        return {"mensaje": "Usuario eliminado"}

    def get_by_email(self, correo):
        return (
            self.db.query(UsuarioModel)
            .filter(UsuarioModel.correo == correo)
            .first()
        )

    def update_auth_fields(self, usuario_id, intentos_fallidos, bloqueado_hasta):
        usuario = (
            self.db.query(UsuarioModel)
            .filter(UsuarioModel.id_usuario == usuario_id)
            .first()
        )

        if not usuario:
            return None

        usuario.intentos_fallidos = intentos_fallidos
        usuario.bloqueado_hasta = bloqueado_hasta

        self.db.flush()
        self.db.refresh(usuario)
        return usuario

    def update_password(self, usuario_id, nuevo_hash):
        usuario = (
            self.db.query(UsuarioModel)
            .filter(UsuarioModel.id_usuario == usuario_id)
            .first()
        )

        if not usuario:
            return None

        usuario.contrasena = nuevo_hash

        self.db.flush()
        self.db.refresh(usuario)
        return usuario

    def contar_admins_activos(self, excluir_id_usuario=None):
        from app.core.security.roles import ROL_ADMIN
        from app.shared.constants.estados import ESTADO_ACTIVO

        consulta = self.db.query(func.count(UsuarioModel.id_usuario)).filter(
            UsuarioModel.estado == ESTADO_ACTIVO,
            UsuarioModel.id_rol == ROL_ADMIN,
        )

        if excluir_id_usuario is not None:
            consulta = consulta.filter(UsuarioModel.id_usuario != excluir_id_usuario)

        return consulta.scalar() or 0
