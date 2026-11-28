from app.core.constants import MAX_INTENTOS_CODIGO_RECUPERACION
from app.core.security.PasswordHasher import PasswordHasher
from app.core.security.password_policy import validate_password
from app.modules.auth.application.use_cases.codigo_recuperacion import (
    hash_codigo_recuperacion,
)
from app.shared.exceptions.auth_errors import (
    ContrasenaInvalidaException,
    InvalidOrExpiredTokenException,
)


class ConfirmPasswordRecoveryUseCase:

    def __init__(self, auth_repository, usuario_repository):
        self.auth_repository = auth_repository
        self.usuario_repository = usuario_repository

    def _registrar_intento_fallido(self, usuario_id):
        codigo_activo = self.auth_repository.find_active_recovery_token(
            usuario_id
        )

        if not codigo_activo:
            return

        intentos = (codigo_activo.intentos_fallidos or 0) + 1
        usado = intentos >= MAX_INTENTOS_CODIGO_RECUPERACION

        self.auth_repository.update_recovery_token_attempts(
            codigo_activo.id,
            intentos,
            usado,
        )

    def execute(self, correo, codigo, nueva_contrasena):
        usuario = self.usuario_repository.get_by_email_recuperacion(correo)

        if not usuario:
            raise InvalidOrExpiredTokenException()

        token_hash = hash_codigo_recuperacion(usuario.id_usuario, codigo)
        reset_token = self.auth_repository.find_valid_token(
            usuario.id_usuario,
            token_hash,
        )

        if not reset_token or not reset_token.es_valido():
            self._registrar_intento_fallido(usuario.id_usuario)
            raise InvalidOrExpiredTokenException()

        try:
            validate_password(nueva_contrasena)
        except ValueError as error:
            raise ContrasenaInvalidaException(str(error))

        nuevo_hash = PasswordHasher.hash(nueva_contrasena)

        self.usuario_repository.update_password(
            reset_token.usuario_id,
            nuevo_hash
        )

        self.usuario_repository.update_auth_fields(
            reset_token.usuario_id,
            0,
            None,
        )

        self.auth_repository.invalidate_token(reset_token.id)

        return {
            "mensaje": "Contraseña restablecida exitosamente"
        }
