class ObtenerCuentaPorIdUseCase:

    def __init__(self, repository):
        self.repository = repository

    def execute(self, id_usuario):

        cuenta = self.repository.get_by_id(id_usuario)

        if cuenta is None:
            return {
                "success": False,
                "message": "Cuenta no encontrada"
            }

        return {
            "success": True,
            "cuenta": cuenta
        }
