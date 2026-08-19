class ActualizarAhorroUseCase:

    def __init__(self, repository):
        self.repository = repository

    def execute(self, id_ahorro, ahorro_data):
        return self.repository.update(id_ahorro, ahorro_data)
