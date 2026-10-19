from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from app.modules.usuario.domain.interface.usuario_repository import UsuarioRepository
from app.modules.usuario.domain.entity.usuario import Usuario
from app.modules.usuario.infrastructure.model.usuario_model import UsuarioModel


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

    def create(self, usuario_data):
        usuario = UsuarioModel(**usuario_data)
        self.db.add(usuario)
        self.db.commit()
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

        return items, total

    def get_by_id(self, id_usuario):
        return (
            self.db.query(UsuarioModel)
            .filter(UsuarioModel.id_usuario == id_usuario)
            .first()
        )

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

        # `flush` deja el cambio dentro de la transacción abierta para que la
        # ruta lo confirme junto con la auditoría en un único commit.
        # El flush debe ir antes del refresh: con autoflush=False un refresh
        # sobre atributos modificados descarta los cambios sin guardarlos.
        self.db.flush()
        self.db.refresh(usuario)

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
        self.db.commit()

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

        self.db.commit()
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

        self.db.commit()
        self.db.refresh(usuario)
        return usuario
