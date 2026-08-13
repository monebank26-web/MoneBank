from app.modules.transaccion.infrastructure.repository.sql_transaccion_repository import (
    SqlTransaccionRepository
)


class RegistrarGasto:

    def __init__(self, repository):
        self.repository = repository

    def execute(self, db, transaccion_data):

        transaccion_data["tipo"] = "gasto"

        return self.repository.create(
            db,
            transaccion_data
        )