from app.modules.cuenta.infrastructure.model.cuenta_model import (
    CuentaModel
)


class CrearUsuario:

    def __init__(self, repository):
        self.repository = repository

    def execute(self, db, usuario_data):

        usuario_data["contrasena"] = PasswordHasher.hash(
            usuario_data["contrasena"]
        )

        # Valores automáticos del usuario
        usuario_data["estado"] = "ACTIVO"
        usuario_data["id_rol"] = 2
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