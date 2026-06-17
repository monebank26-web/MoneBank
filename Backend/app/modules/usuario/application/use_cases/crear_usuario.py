from app.modules.usuario.infrastucture.repository.sql_usuario_repository import (
    SqlUsuarioRepository
)

from app.modules.cuenta.infrastucture.model.cuenta_model import (
    CuentaModel
)


class CrearUsuario:

    def __init__(self):
        self.repository = SqlUsuarioRepository()

    def execute(self, db, usuario_data):

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