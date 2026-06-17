class LoginUsuarioUseCase:

    def __init__(self, repository):
        self.repository = repository

    def execute(self, db, correo, contrasena):

        usuario = self.repository.login(
            db,
            correo,
            contrasena
        )

        print("USUARIO ENCONTRADO:", usuario)

        if not usuario:
            return {
                "success": False,
                "message": "Credenciales incorrectas"
            }

        return {
            "success": True,
            "usuario": usuario
        }