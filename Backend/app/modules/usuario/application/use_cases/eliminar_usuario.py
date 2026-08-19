class EliminarUsuarioUseCase:

    def __init__(self, repository):
        self.repository = repository

    def execute(self, id_usuario):

        if id_usuario <= 0:
            return {
                "success": False,
                "message": "Id inválido"
            }

        usuario = self.repository.get_by_id(id_usuario)

        if not usuario:
            return {
                "success": False,
                "message": "Usuario no encontrado"
            }

        self.repository.delete(id_usuario)

        return {
            "success": True,
            "message": "Usuario eliminado correctamente"
        }
