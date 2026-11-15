from unittest.mock import Mock, patch

from app.core.config.settings import settings
from app.core.constants import MINUTOS_TOKEN_RECUPERACION
from app.core.dependencies.email_service import EmailService


@patch("app.core.dependencies.email_service.smtplib.SMTP_SSL")
def test_envia_correo_de_restablecimiento_administrativo(mock_smtp):
    mensaje_enviado = {}
    servidor = Mock()

    def capturar_mensaje(mensaje):
        mensaje_enviado["mensaje"] = mensaje

    servidor.send_message.side_effect = capturar_mensaje
    mock_smtp.return_value.__enter__.return_value = servidor

    resultado = EmailService().send_password_reset_by_admin(
        "usuario@test.com",
        "token-seguro",
    )

    assert resultado is True
    mock_smtp.assert_called_once_with("smtp.gmail.com", 465)
    servidor.login.assert_called_once()

    mensaje = mensaje_enviado["mensaje"]
    assert mensaje["To"] == "usuario@test.com"
    assert "administrador" in mensaje["Subject"].lower()

    partes = mensaje.get_payload()
    texto = partes[0].get_payload(decode=True).decode("utf-8")
    html = partes[1].get_payload(decode=True).decode("utf-8")

    assert "un administrador solicitó restablecer la contraseña" in (
        texto.lower()
    )
    assert "tu contraseña actual sigue funcionando" in texto.lower()
    assert "http://localhost:3000/recuperar?token=token-seguro" in texto
    assert (
        f"vence en {MINUTOS_TOKEN_RECUPERACION} minutos"
        in texto.lower()
    )
    assert "crear nueva contraseña" in html.lower()
    assert "http://localhost:3000/recuperar?token=token-seguro" in html
    assert "si no esperabas este correo, ignóralo" in texto.lower()
    assert "avisa al administrador" in texto.lower()
    assert "soporte" not in texto.lower()
    assert "contraseña anterior ya no funciona" not in texto.lower()


@patch(
    "app.core.dependencies.email_service.smtplib.SMTP_SSL",
    side_effect=Exception("SMTP no disponible"),
)
def test_fallo_al_enviar_correo_administrativo_devuelve_false(mock_smtp):
    resultado = EmailService().send_password_reset_by_admin(
        "usuario@test.com",
        "token-seguro",
    )

    assert resultado is False


@patch("app.core.dependencies.email_service.smtplib.SMTP_SSL")
def test_envia_correo_de_recuperacion_con_la_url_por_defecto(mock_smtp):
    mensaje_enviado = {}
    servidor = Mock()

    def capturar_mensaje(mensaje):
        mensaje_enviado["mensaje"] = mensaje

    servidor.send_message.side_effect = capturar_mensaje
    mock_smtp.return_value.__enter__.return_value = servidor

    resultado = EmailService().send_recovery_email(
        "usuario@test.com",
        "token-seguro",
    )

    assert resultado is True
    cuerpo = mensaje_enviado["mensaje"].get_payload(decode=True).decode(
        "utf-8"
    )
    assert "http://localhost:3000/recuperar?token=token-seguro" in cuerpo


@patch("app.core.dependencies.email_service.smtplib.SMTP_SSL")
def test_usa_la_url_del_frontend_configurada_en_ambos_correos(mock_smtp):
    mensajes_enviados = []
    servidor = Mock()
    servidor.send_message.side_effect = mensajes_enviados.append
    mock_smtp.return_value.__enter__.return_value = servidor
    url_configurada = "https://panel.monebank.test/"

    with patch.object(settings, "FRONTEND_URL", url_configurada):
        email_service = EmailService()
        email_service.send_recovery_email("usuario@test.com", "token-1")
        email_service.send_password_reset_by_admin(
            "usuario@test.com",
            "token-2",
        )

    recuperacion = mensajes_enviados[0].get_payload(decode=True).decode(
        "utf-8"
    )
    partes_admin = mensajes_enviados[1].get_payload()
    texto_admin = partes_admin[0].get_payload(decode=True).decode("utf-8")

    assert (
        "https://panel.monebank.test/recuperar?token=token-1"
        in recuperacion
    )
    assert (
        "https://panel.monebank.test/recuperar?token=token-2"
        in texto_admin
    )
