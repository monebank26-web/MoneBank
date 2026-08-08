from app.core.security.JwtManager import JwtManager
from app.core.security.PasswordHasher import PasswordHasher


class LoginUsuarioUseCase:

    def __init__(self, repository):
        self.repository = repository

    def execute(self, db, correo, contrasena):

        usuario = self.repository.login(
            db,
            correo
        )

        if not usuario:
            return {
                "success": False,
                "message": "Credenciales incorrectas"
            }

        if not PasswordHasher.verify(
            contrasena,
            usuario.contrasena
        ):
            return {
                "success": False,
                "message": "Credenciales incorrectas"
            }

        token = JwtManager.create_token({
            "sub": str(usuario.id_usuario),
            "correo": usuario.correo,
            "id_rol": usuario.id_rol,
        })

        return {
            "success": True,
            "token": token,
            "usuario": {
                "id_usuario": usuario.id_usuario,
                "nombres": usuario.nombres,
                "apellidos": usuario.apellidos,
                "correo": usuario.correo,
                "estado": usuario.estado,
                "id_rol": usuario.id_rol,
                "id_tipo_usuario": usuario.id_tipo_usuario,
            }
        }
