from app.modules.ahorro.infrastucture.repository.sql_ahorro_repository import (
    SqlAhorroRepository
)

class CrearAhorro:

    def __init__(self):
        self.repository = SqlAhorroRepository()

    def execute(self, db, ahorro_data):
        return self.repository.create(
            db,
            ahorro_data
        )