import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.core.config.settings import settings
from app.core.constants import MINUTOS_TOKEN_RECUPERACION


class EmailService:

    def send_recovery_email(self, correo: str, token: str):
        logger = logging.getLogger(__name__)

        link = f"http://localhost:3000/recuperar?token={token}"

        msg = MIMEText(
            f"<h2>MoneBank - Recuperacion de contrasena</h2>"
            f"<p>Haz clic en el enlace para restablecer tu contrasena:</p>"
            f"<p><a href='{link}'>{link}</a></p>"
            f"<p>Este enlace expira en 15 minutos.</p>",
            "html"
        )
        msg["Subject"] = "MoneBank - Recuperación de contraseña"
        msg["From"] = settings.EMAIL_USER
        msg["To"] = correo

        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(settings.EMAIL_USER, settings.EMAIL_PASSWORD)
                server.send_message(msg)
            logger.info(f"Email de recuperación enviado a {correo}")
            return True
        except Exception as e:
            logger.error(f"Error al enviar email a {correo}: {e}")
            return False

    def send_password_reset_by_admin(self, correo: str, token: str):
        logger = logging.getLogger(__name__)

        link = f"http://localhost:3000/recuperar?token={token}"

        texto = (
            "Hola:\n\n"
            "Un administrador solicitó restablecer la contraseña de tu "
            "cuenta MoneBank.\n\n"
            "Tu contraseña actual sigue funcionando hasta que crees una "
            "nueva.\n"
            "Para crear una nueva contraseña, abre este enlace:\n"
            f"{link}\n\n"
            f"El enlace vence en {MINUTOS_TOKEN_RECUPERACION} minutos y "
            "solo puede usarse una vez.\n\n"
            "Si no esperabas este correo, ignóralo: tu contraseña actual "
            "no cambia mientras no uses el enlace. Si crees que alguien "
            "intenta acceder a tu cuenta, avisa al administrador.\n"
        )

        html = (
            "<h2>MoneBank - Restablecimiento de contraseña</h2>"
            "<p>Un administrador solicitó restablecer la contraseña de tu "
            "cuenta.</p>"
            "<p><strong>Tu contraseña actual sigue funcionando</strong> "
            "hasta que crees una nueva.</p>"
            f"<p><a href='{link}' style='display:inline-block;"
            "padding:12px 24px;background:#c9a84c;color:#080808;"
            "text-decoration:none;border-radius:6px;font-weight:bold;'>"
            "Crear nueva contraseña</a></p>"
            "<p>Si el botón no funciona, copia y pega este enlace:<br>"
            f"<a href='{link}'>{link}</a></p>"
            f"<p>Este enlace vence en {MINUTOS_TOKEN_RECUPERACION} minutos "
            "y solo puede usarse una vez.</p>"
            "<p>Si no esperabas este correo, ignóralo: tu contraseña actual "
            "no cambia mientras no uses el enlace. Si crees que alguien "
            "intenta acceder a tu cuenta, avisa al administrador.</p>"
        )

        msg = MIMEMultipart("alternative")
        msg.attach(MIMEText(texto, "plain", "utf-8"))
        msg.attach(MIMEText(html, "html", "utf-8"))
        msg["Subject"] = (
            "MoneBank - Restablecimiento de contraseña por administrador"
        )
        msg["From"] = settings.EMAIL_USER
        msg["To"] = correo

        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(settings.EMAIL_USER, settings.EMAIL_PASSWORD)
                server.send_message(msg)
            logger.info(
                "Email de restablecimiento administrativo enviado a %s",
                correo,
            )
            return True
        except Exception as error:
            logger.error(
                "Error al enviar email de restablecimiento a %s: %s",
                correo,
                error,
            )
            return False

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
