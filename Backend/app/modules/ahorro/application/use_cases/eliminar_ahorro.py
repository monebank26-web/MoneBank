class EliminarAhorroUseCase:

    def __init__(self, repository):
        self.repository = repository

    def execute(self, id_ahorro):
        return self.repository.delete(id_ahorro)
