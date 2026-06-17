from app.modules.cuenta.infrastucture.repository.sql_cuenta_repository import (
    SqlCuentaRepository
)

class CrearCuenta:

    def __init__(self):
        self.repository = SqlCuentaRepository()

    def execute(
        self,
        db,
        cuenta_data
    ):
        return self.repository.create(
            db,
            cuenta_data
        )