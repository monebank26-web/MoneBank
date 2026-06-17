class ObtenerUsuarioPorIdUseCase:

    def __init__(self, repository):
        self.repository = repository

    def execute(self, db, id_usuario):
        return self.repository.get_by_id(db, id_usuario)