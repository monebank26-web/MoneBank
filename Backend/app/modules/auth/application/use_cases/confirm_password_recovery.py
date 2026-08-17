from app.core.security.PasswordHasher import PasswordHasher
from app.core.security.password_policy import validate_password
from app.core.security.token_generator import TokenGenerator
from app.shared.exceptions.business_exceptions import InvalidOrExpiredTokenException


class ConfirmPasswordRecoveryUseCase:

    def __init__(self, auth_repository, usuario_repository):
        self.auth_repository = auth_repository
        self.usuario_repository = usuario_repository

    def execute(self, token, nueva_contrasena):

        token_hash = TokenGenerator.hash(token)

        reset_token = self.auth_repository.find_valid_token(token_hash)

        if not reset_token:
            raise InvalidOrExpiredTokenException()

        if reset_token.esta_expirado():
            raise InvalidOrExpiredTokenException()

        if reset_token.fue_utilizado():
            raise InvalidOrExpiredTokenException()

        validate_password(nueva_contrasena)

        nuevo_hash = PasswordHasher.hash(nueva_contrasena)

        self.usuario_repository.update_password(
            reset_token.usuario_id,
            nuevo_hash
        )

        self.auth_repository.invalidate_token(reset_token.id)

        return {
            "mensaje": "Contraseña restablecida exitosamente"
        }
