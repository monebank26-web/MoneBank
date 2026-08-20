from datetime import datetime, timedelta, timezone

from app.core.constants import MINUTOS_TOKEN_RECUPERACION
from app.core.security.reset_token import TokenGenerator
from app.shared.exceptions.business_exceptions import EmailNotFoundException


class RequestPasswordRecoveryUseCase:

    def __init__(self, auth_repository, usuario_repository, email_service):
        self.auth_repository = auth_repository
        self.usuario_repository = usuario_repository
        self.email_service = email_service

    def execute(self, correo):

        usuario = self.usuario_repository.get_by_email(correo)

        if not usuario:
            raise EmailNotFoundException()

        self.auth_repository.invalidate_user_tokens(usuario.id_usuario)

        token_original = TokenGenerator.generate()
        token_hash = TokenGenerator.hash(token_original)

        fecha_expiracion = (
            datetime.now(timezone.utc)
            + timedelta(minutes=MINUTOS_TOKEN_RECUPERACION)
        )

        self.auth_repository.create_recovery_token(
            usuario.id_usuario,
            token_hash,
            fecha_expiracion
        )

        self.email_service.send_recovery_email(correo, token_original)

        return {
            "mensaje": (
                "Si el correo está registrado, "
                "recibirás un enlace de recuperación"
            )
        }
