class EliminarUsuarioUseCase:

    def __init__(self, repository):
        self.repository = repository

    def execute(self, db, id_usuario):
        return self.repository.delete(
            db,
            id_usuario
        )