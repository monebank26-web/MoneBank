from app.modules.cuenta.infrastructure.repository.sql_cuenta_repository import (
    SqlCuentaRepository
)

class CrearCuenta:

    def __init__(self, repository):
        self.repository = repository

    def execute(
        self,
        db,
        cuenta_data
    ):
        return self.repository.create(
            db,
            cuenta_data
        )