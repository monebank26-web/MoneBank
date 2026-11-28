import logging

from app.modules.auth.application.use_cases.codigo_recuperacion import (
    crear_codigo_recuperacion,
)

logger = logging.getLogger(__name__)

MENSAJE_SOLICITUD_RECUPERACION = (
    "Si el correo está registrado, recibirás un código"
)


class RequestPasswordRecoveryUseCase:

    def __init__(self, auth_repository, usuario_repository, email_service):
        self.auth_repository = auth_repository
        self.usuario_repository = usuario_repository
        self.email_service = email_service

    def execute(self, correo):
        resultado = {
            "mensaje": MENSAJE_SOLICITUD_RECUPERACION,
            "_correo_enviado": True,
        }

        usuario = self.usuario_repository.get_by_email_recuperacion(correo)

        if not usuario:
            return resultado

        codigo = crear_codigo_recuperacion(
            self.auth_repository,
            usuario.id_usuario,
        )

        if codigo is None:
            return resultado

        try:
            enviado = self.email_service.send_recovery_email(
                usuario.correo,
                codigo,
            )
        except Exception:
            logger.exception(
                "Error inesperado al enviar el código de recuperación"
            )
            enviado = False

        if not enviado:
            logger.warning(
                "No se pudo enviar el código de recuperación a %s",
                usuario.correo,
            )
            resultado["_correo_enviado"] = False

        return resultado
