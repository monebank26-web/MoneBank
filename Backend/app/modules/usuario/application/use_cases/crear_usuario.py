from app.core.security.PasswordHasher import PasswordHasher
from app.core.security.roles import ROL_USUARIO
from app.modules.cuenta.infrastructure.model.cuenta_model import (
    CuentaModel
)
from app.shared.exceptions.business_exceptions import EmailAlreadyExistsException


class CrearUsuario:

    def __init__(self, repository):
        self.repository = repository

    def execute(self, db, usuario_data):

        if self.repository.exists_by_email(db, usuario_data["correo"]):
            raise EmailAlreadyExistsException()

        usuario_data["contrasena"] = PasswordHasher.hash(
            usuario_data["contrasena"]
        )

        usuario_data["estado"] = "ACTIVO"
        usuario_data["id_rol"] = ROL_USUARIO
        usuario_data["id_tipo_usuario"] = 3

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