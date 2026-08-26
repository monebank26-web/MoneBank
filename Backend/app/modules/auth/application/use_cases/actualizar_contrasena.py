from app.core.security.PasswordHasher import PasswordHasher
from app.core.security.password_policy import validate_password
from app.modules.usuario.domain.interface.usuario_repository import UsuarioRepository
from app.shared.exceptions.business_exceptions import (
    InvalidCredentialsException,
    UsuarioNotFoundException,
)



class ActualizarContrasenaUseCase:

    def __init__(self, repository: UsuarioRepository):
        self.repository = repository

    def execute(
        self,
        id_usuario,
        contrasena_actual,
        contrasena_nueva
    ):
        usuario = self.repository.get_by_id(id_usuario)

        if not usuario:
            raise UsuarioNotFoundException()
        
        if not PasswordHasher.verify(contrasena_actual, usuario.contrasena):
            raise InvalidCredentialsException()

        validate_password(contrasena_nueva)

        nuevo_hash = PasswordHasher.hash(contrasena_nueva)

        self.repository.update_password(id_usuario, nuevo_hash)

        return {"mensaje": "Contraseña actualizada exitosamente"}
