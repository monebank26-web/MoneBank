class ObtenerAhorroPorIdUseCase:

    def __init__(self, repository):
        self.repository = repository

    def execute(
        self,
        db,
        id_ahorro
    ):
        return self.repository.get_by_id(
            db,
            id_ahorro
        )