class ObtenerCuentaPorIdUseCase:

    def __init__(self, repository):
        self.repository = repository

    def execute(self, id_cuenta):

        if id_cuenta <= 0:
            return {
                "success": False,
                "message": "Id inválido"
            }

        cuenta = self.repository.get_by_id(id_cuenta)

        if cuenta is None:
            return {
                "success": False,
                "message": "Cuenta no encontrada"
            }

        return {
            "success": True,
            "cuenta": cuenta
        }
