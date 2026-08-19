class ObtenerUsuarioPorIdUseCase:

    def __init__(self, repository):
        self.repository = repository

    def execute(self, id_usuario):
        return self.repository.get_by_id(id_usuario)
