
class LoginUsuarioUseCase:

    def __init__(self, repository):
        self.repository = repository

    def execute(self, db, correo, contrasena):

        usuario = self.repository.buscar_por_correo(
            db,
            correo
        )

        if not usuario:
            return {
                "success": False,
                "message": "Credenciales incorrectas"
            }

        if usuario["contrasena"] != contrasena:
            return {
                "success": False,
                "message": "Credenciales incorrectas"
            }

        return {
            "success": True,
            "usuario": usuario
        }