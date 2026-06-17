class ActualizarUsuarioUseCase:

    def __init__(self, repository):
        self.repository = repository

    def execute(
        self,
        db,
        id_usuario,
        usuario_data
    ):
        return self.repository.update(
            db,
            id_usuario,
            usuario_data
        )