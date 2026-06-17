class ObtenerCuentaPorIdUseCase:

    def __init__(self, repository):
        self.repository = repository

    def execute(
        self,
        db,
        id_cuenta
    ):
        return self.repository.get_by_id(
            db,
            id_cuenta
        )