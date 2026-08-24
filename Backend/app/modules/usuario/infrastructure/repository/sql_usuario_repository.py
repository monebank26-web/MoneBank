from sqlalchemy.orm import Session

from app.modules.usuario.domain.interface.usuario_repository import UsuarioRepository
from app.modules.usuario.domain.entity.usuario import Usuario
from app.modules.usuario.infrastructure.model.usuario_model import UsuarioModel


class SqlUsuarioRepository(UsuarioRepository):

    def __init__(self, db: Session):
        self.db = db

    def create(self, usuario_data):
        usuario = UsuarioModel(**usuario_data)
        self.db.add(usuario)
        self.db.commit()
        self.db.refresh(usuario)
        return usuario

    def exists_by_email(self, correo):
        return (
            self.db.query(UsuarioModel.id_usuario)
            .filter(UsuarioModel.correo == correo)
            .first()
            is not None
        )

    def get_all(self):
        return self.db.query(UsuarioModel).all()

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

        self.db.commit()
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
