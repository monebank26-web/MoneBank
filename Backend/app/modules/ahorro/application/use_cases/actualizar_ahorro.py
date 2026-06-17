class ActualizarAhorroUseCase:

    def __init__(self, repository):
        self.repository = repository

    def execute(
        self,
        db,
        id_ahorro,
        ahorro_data
    ):
        return self.repository.update(
            db,
            id_ahorro,
            ahorro_data
        )