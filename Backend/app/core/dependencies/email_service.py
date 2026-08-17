import logging
import smtplib
from email.mime.text import MIMEText

from app.core.config.settings import settings


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
