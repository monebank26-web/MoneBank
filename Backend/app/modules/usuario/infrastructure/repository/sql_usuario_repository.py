from sqlalchemy.orm import Session

from app.modules.usuario.domain.interface.usuario_repository import UsuarioRepository
from app.modules.usuario.domain.entity.usuario import Usuario

from app.modules.usuario.infrastructure.model.usuario_model import UsuarioModel



class SqlUsuarioRepository(UsuarioRepository):

    def __init__(self, db: Session):
        self.db = db

    def create(self, db, usuario_data):
        usuario = UsuarioModel(**usuario_data)

        db.add(usuario)
        db.commit()
        db.refresh(usuario)

        return usuario

    def exists_by_email(self, db, correo):
        return (
            db.query(UsuarioModel.id_usuario)
            .filter(UsuarioModel.correo == correo)
            .first()
            is not None
        )
    
    def get_all(self, db):
        return db.query(UsuarioModel).all()
    
    def get_by_id(self, db, id_usuario):
        return (
            db.query(UsuarioModel)
            .filter(
                UsuarioModel.id_usuario == id_usuario
            )
            .first()
        )
    
    def update(
        self,
        id_usuario,
        usuario_data
    ):

        usuario = (
            self.db.query(UsuarioModel)
            .filter(
                UsuarioModel.id_usuario == id_usuario
            )
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
    
    def delete(
        self,
        db,
        id_usuario
    ):

        usuario = (
            db.query(UsuarioModel)
            .filter(
                UsuarioModel.id_usuario == id_usuario
            )
            .first()
        )

        if not usuario:
            return None

        db.delete(usuario)
        db.commit()

        return {
            "mensaje": "Usuario eliminado"
        }
    
    def get_by_email(self, db, correo):
        return (
            db.query(UsuarioModel)
            .filter(UsuarioModel.correo == correo)
            .first()
        )