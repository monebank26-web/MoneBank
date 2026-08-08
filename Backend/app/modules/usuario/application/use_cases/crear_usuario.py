from app.modules.usuario.infrastructure.repository.sql_usuario_repository import (
    SqlUsuarioRepository
)

from app.modules.cuenta.infrastructure.model.cuenta_model import (
    CuentaModel
)

from app.core.security.PasswordHasher import PasswordHasher


class CrearUsuario:

    def __init__(self):
        self.repository = SqlUsuarioRepository()

    def execute(self, db, usuario_data):

        usuario_data["contrasena"] = PasswordHasher.hash(
            usuario_data["contrasena"]
        )

        usuario = self.repository.create(
            db,
            usuario_data
        )

        cuenta = CuentaModel(
            saldo=0,
            estado="ACTIVA",
            id_usuario=usuario.id_usuario
        )

        db.add(cuenta)
        db.commit()
        db.refresh(cuenta)

        return usuario