import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.core.config.settings import settings
from app.core.constants import MINUTOS_TOKEN_RECUPERACION


class EmailService:

    def _construir_correo_recuperacion(
        self,
        correo,
        codigo,
        asunto,
        titulo,
        introduccion,
        instruccion,
        detalle_extra=None,
    ):
        vigencia = (
            f"Vence en {MINUTOS_TOKEN_RECUPERACION} minutos y solo puede "
            "usarse una vez."
        )

        texto = (
            f"{titulo}\n\n"
            "Hola:\n\n"
            f"{introduccion}\n\n"
            "Tu código es:\n"
            f"{codigo}\n\n"
            f"{vigencia}\n\n"
            f"{instruccion}\n"
        )

        if detalle_extra:
            texto += f"\n{detalle_extra}\n"

        texto += "\nSi no lo esperabas, ignóralo.\n"

        detalle_html = f"<p>{detalle_extra}</p>" if detalle_extra else ""
        html = (
            "<!doctype html>"
            '<html lang="es">'
            "<head>"
            '<meta charset="utf-8">'
            f"<title>{titulo}</title>"
            "</head>"
            "<body>"
            f"<h1>{titulo}</h1>"
            f"<p>{introduccion}</p>"
            "<p><strong>Tu código es:</strong></p>"
            '<p style="font-size:32px;font-weight:bold;'
            'letter-spacing:6px;">'
            f"{codigo}</p>"
            f"<p>{vigencia}</p>"
            f"<p>{instruccion}</p>"
            f"{detalle_html}"
            "<p>Si no lo esperabas, ignóralo.</p>"
            "</body></html>"
        )

        msg = MIMEMultipart("alternative")
        msg.attach(MIMEText(texto, "plain", "utf-8"))
        msg.attach(MIMEText(html, "html", "utf-8"))
        msg["Subject"] = asunto
        msg["From"] = settings.EMAIL_USER
        msg["To"] = correo

        return msg

    def _enviar_correo(self, msg, correo, tipo):
        logger = logging.getLogger(__name__)

        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(settings.EMAIL_USER, settings.EMAIL_PASSWORD)
                server.send_message(msg)
            logger.info("%s enviado a %s", tipo, correo)
            return True
        except Exception as error:
            logger.error(
                "Error al enviar %s a %s: %s",
                tipo,
                correo,
                error,
            )
            return False

    def send_recovery_email(self, correo: str, codigo: str):
        instruccion = (
            "Para crear una nueva contraseña, abre MoneBank, pulsa "
            "'¿Olvidaste tu contraseña?' en el inicio de sesión y escribe "
            "tu correo y este código."
        )
        msg = self._construir_correo_recuperacion(
            correo=correo,
            codigo=codigo,
            asunto="MoneBank - Código de recuperación de contraseña",
            titulo="MoneBank - Recuperación de contraseña",
            introduccion=(
                "Solicitaste restablecer la contraseña de tu cuenta "
                "MoneBank."
            ),
            instruccion=instruccion,
        )

        return self._enviar_correo(
            msg,
            correo,
            "código de recuperación",
        )

    def send_password_reset_by_admin(self, correo: str, codigo: str):
        instruccion = (
            "Para crear una nueva contraseña, abre MoneBank, pulsa "
            "'¿Olvidaste tu contraseña?' y luego 'Ya tengo un código' en el "
            "inicio de sesión y escribe tu correo y este código."
        )
        msg = self._construir_correo_recuperacion(
            correo=correo,
            codigo=codigo,
            asunto="MoneBank - Código de restablecimiento de contraseña",
            titulo="MoneBank - Restablecimiento de contraseña",
            introduccion=(
                "Un administrador inició el restablecimiento de la "
                "contraseña de tu cuenta MoneBank. Tu contraseña actual "
                "sigue funcionando hasta que uses el código."
            ),
            instruccion=instruccion,
            detalle_extra=(
                "No pidas otro código: el que recibiste ya es válido."
            ),
        )

        return self._enviar_correo(
            msg,
            correo,
            "código de restablecimiento administrativo",
        )

    def send_parental_code(self, correo: str, codigo: str, operacion: str):
        from email.mime.text import MIMEText
        import logging
        msg = MIMEText(f"<h2>MoneBank - Código de {operacion}</h2><p>Tu código es:</p><h1>{codigo}</h1><p>Expira en 15 minutos y solo puede usarse una vez.</p>", "html")
        msg["Subject"] = f"MoneBank - Código de {operacion}"
        msg["From"] = settings.EMAIL_USER
        msg["To"] = correo
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(settings.EMAIL_USER, settings.EMAIL_PASSWORD)
                server.send_message(msg)
            return True
        except Exception as error:
            logging.getLogger(__name__).error("Error enviando código parental: %s", error)
            return False


def get_email_service() -> EmailService:
    return EmailService()
