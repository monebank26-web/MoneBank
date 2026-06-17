class EliminarAhorroUseCase:

    def __init__(self, repository):
        self.repository = repository

    def execute(
        self,
        db,
        id_ahorro
    ):
        return self.repository.delete(
            db,
            id_ahorro
        )