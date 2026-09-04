from unittest.mock import Mock

from google import genai
import pytest

from app.modules.chat_ia.infrastructure.ia.gemini_chat_service import (
    GeminiChatService
)
from app.shared.exceptions.business_exceptions import ConsejoIANoDisponible


def crear_respuesta_gemini(texto):
    respuesta = Mock()
    respuesta.text = texto
    return respuesta


def cliente_falso(texto=None, error=None):
    cliente = Mock()
    if error is not None:
        cliente.models.generate_content.side_effect = error
    else:
        cliente.models.generate_content.return_value = crear_respuesta_gemini(texto)
    return cliente


def test_generar_respuesta_devuelve_texto_limpio(monkeypatch):
    cliente = cliente_falso("  Hola, te ayudo.  ")

    def factory(**kwargs):
        return cliente

    monkeypatch.setattr(genai, "Client", factory)

    servicio = GeminiChatService("clave-falsa", "gemini-3.5-flash-lite")
    resultado = servicio.generar_respuesta(
        {"saldo_actual": 1000},
        [{"role": "user", "parts": [{"text": "hola"}]}],
    )

    assert resultado == "Hola, te ayudo."
    llamada = cliente.models.generate_content.call_args
    assert llamada.kwargs["contents"] == [{"role": "user", "parts": [{"text": "hola"}]}]
    assert llamada.kwargs["config"].system_instruction


def test_sin_api_key_no_crea_cliente(monkeypatch):
    def client_falso(**kwargs):
        raise AssertionError("No debe crear el cliente sin api key")

    monkeypatch.setattr(genai, "Client", client_falso)

    servicio = GeminiChatService("", "gemini-3.5-flash-lite")

    with pytest.raises(ConsejoIANoDisponible):
        servicio.generar_respuesta({"saldo_actual": 1000}, [])


def test_respuesta_vacia_se_convierte_en_no_disponible(monkeypatch):
    monkeypatch.setattr(
        genai, "Client", lambda **kwargs: cliente_falso(texto="")
    )

    servicio = GeminiChatService("clave-falsa", "gemini-3.5-flash-lite")

    with pytest.raises(ConsejoIANoDisponible):
        servicio.generar_respuesta({"saldo_actual": 1000}, [])


def test_error_de_red_se_convierte_en_no_disponible(monkeypatch):
    from google.genai import errors

    monkeypatch.setattr(
        genai,
        "Client",
        lambda **kwargs: cliente_falso(
            error=errors.ClientError(503, {"error": {}})
        ),
    )

    servicio = GeminiChatService("clave-falsa", "gemini-3.5-flash-lite")

    with pytest.raises(ConsejoIANoDisponible):
        servicio.generar_respuesta({"saldo_actual": 1000}, [])
