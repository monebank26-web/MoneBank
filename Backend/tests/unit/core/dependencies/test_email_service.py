from unittest.mock import Mock, patch

from app.core.constants import MINUTOS_TOKEN_RECUPERACION
from app.core.dependencies.email_service import EmailService


def capturar_mensaje(mock_smtp):
    mensaje_enviado = {}
    servidor = Mock()

    def guardar(mensaje):
        mensaje_enviado["mensaje"] = mensaje

    servidor.send_message.side_effect = guardar
    mock_smtp.return_value.__enter__.return_value = servidor

    return mensaje_enviado, servidor


def partes_del_mensaje(mensaje):
    partes = mensaje.get_payload()
    texto = partes[0].get_payload(decode=True).decode("utf-8")
    html = partes[1].get_payload(decode=True).decode("utf-8")
    return texto, html


@patch("app.core.dependencies.email_service.smtplib.SMTP_SSL")
def test_envia_correo_de_restablecimiento_administrativo(mock_smtp):
    mensaje_enviado, servidor = capturar_mensaje(mock_smtp)

    resultado = EmailService().send_password_reset_by_admin(
        "usuario@test.com",
        "654321",
    )

    assert resultado is True
    mock_smtp.assert_called_once_with("smtp.gmail.com", 465)
    servidor.login.assert_called_once()

    mensaje = mensaje_enviado["mensaje"]
    assert mensaje["To"] == "usuario@test.com"
    assert "restablecimiento" in mensaje["Subject"].lower()
    assert mensaje.is_multipart() is True

    texto, html = partes_del_mensaje(mensaje)

    assert "un administrador inició el restablecimiento" in texto.lower()
    assert "tu contraseña actual sigue funcionando" in texto.lower()
    assert "Tu código es:" in texto
    assert "654321" in texto
    assert (
        f"Vence en {MINUTOS_TOKEN_RECUPERACION} minutos"
        in texto
    )
    assert "solo puede usarse una vez" in texto.lower()
    assert (
        "Para crear una nueva contraseña, abre MoneBank, pulsa "
        "'¿Olvidaste tu contraseña?' en el inicio de sesión y escribe "
        "tu correo y este código."
    ) in texto
    assert (
        "No pidas otro código: el que recibiste ya es válido."
    ) in texto
    assert "Si no lo esperabas, ignóralo." in texto

    assert '<html lang="es">' in html
    assert (
        "<title>MoneBank - Restablecimiento de contraseña</title>"
        in html
    )
    assert "654321" in html
    assert "No pidas otro código" in html

    for contenido in (texto.lower(), html.lower()):
        assert "http" not in contenido
        assert "enlace" not in contenido
        assert "token" not in contenido


@patch(
    "app.core.dependencies.email_service.smtplib.SMTP_SSL",
    side_effect=Exception("SMTP no disponible"),
)
def test_fallo_al_enviar_correo_administrativo_devuelve_false(mock_smtp):
    resultado = EmailService().send_password_reset_by_admin(
        "usuario@test.com",
        "654321",
    )

    assert resultado is False


@patch("app.core.dependencies.email_service.smtplib.SMTP_SSL")
def test_envia_correo_de_recuperacion_con_codigo_sin_url(mock_smtp):
    mensaje_enviado, _ = capturar_mensaje(mock_smtp)

    resultado = EmailService().send_recovery_email(
        "usuario@test.com",
        "000042",
    )

    assert resultado is True
    mensaje = mensaje_enviado["mensaje"]
    assert mensaje.is_multipart() is True

    texto, html = partes_del_mensaje(mensaje)

    assert '<html lang="es">' in html
    assert (
        "<title>MoneBank - Recuperación de contraseña</title>"
        in html
    )
    assert "Tu código es:" in texto
    assert "000042" in texto
    assert "000042" in html
    assert (
        f"Vence en {MINUTOS_TOKEN_RECUPERACION} minutos"
        in texto
    )
    assert "solo puede usarse una vez" in texto.lower()
    assert (
        "Para crear una nueva contraseña, abre MoneBank, pulsa "
        "'¿Olvidaste tu contraseña?' en el inicio de sesión y escribe "
        "tu correo y este código."
    ) in texto
    assert "Si no lo esperabas, ignóralo." in texto

    for contenido in (texto.lower(), html.lower()):
        assert "http" not in contenido
        assert "enlace" not in contenido
        assert "token" not in contenido
