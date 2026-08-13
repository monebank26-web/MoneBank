from app.modules.usuario.infrastructure.model.usuario_model import UsuarioModel


class SqlUsuarioRepository:

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
        db,
        id_usuario,
        usuario_data
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

        for key, value in usuario_data.items():
            setattr(usuario, key, value)

        db.commit()
        db.refresh(usuario)

        return usuario
    
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