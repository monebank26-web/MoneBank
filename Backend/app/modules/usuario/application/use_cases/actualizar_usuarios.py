from app.modules.usuario.domain.interface.usuario_repository import UsuarioRepository
from app.core.security.PasswordHasher import PasswordHasher


class ActualizarUsuarioUseCase:

    def __init__(self, repository: UsuarioRepository):
        self.repository = repository

    def execute(
        self,
        id_usuario,
        usuario_data
    ):
        if "contrasena" in usuario_data:
            if not usuario_data["contrasena"]:
                usuario_data.pop("contrasena")
            else:
                usuario_data["contrasena"] = PasswordHasher.hash(
                    usuario_data["contrasena"]
                )

        Actualizar_usuario = self.repository.update(
            id_usuario,
            usuario_data
        )   
        return Actualizar_usuario