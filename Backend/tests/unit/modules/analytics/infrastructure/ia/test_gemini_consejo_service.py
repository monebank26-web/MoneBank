from unittest.mock import Mock

from google import genai
import pytest

from app.modules.analytics.infrastructure.ia.gemini_consejo_service import (
    GeminiConsejoService
)
from app.shared.exceptions.business_exceptions import ConsejoIANoDisponible


def crear_respuesta_gemini(texto):
    respuesta = Mock()
    respuesta.text = texto
    return respuesta


def cliente_falso(texto=None, respuesta=None, error=None):
    cliente = Mock()
    if error is not None:
        cliente.models.generate_content.side_effect = error
    else:
        cliente.models.generate_content.return_value = (
            respuesta if respuesta is not None else crear_respuesta_gemini(texto)
        )
    return cliente


def test_generar_consejo_devuelve_el_texto_de_gemini(monkeypatch):
    monkeypatch.setattr(
        genai, "Client", lambda **kwargs: cliente_falso("  Tu gasto está dentro de lo normal.  ")
    )

    servicio = GeminiConsejoService("clave-falsa", "gemini-3.7-flash")
    resultado = servicio.generar_consejo({"monto": 50000})

    assert resultado == "Tu gasto está dentro de lo normal."


def test_generar_consejo_sin_api_key_falla_sin_llamar_red(monkeypatch):
    cliente = cliente_falso(texto="no debe llamarse")

    def client_falso(**kwargs):
        raise AssertionError("No debe crear el cliente sin api key")

    monkeypatch.setattr(genai, "Client", client_falso)

    servicio = GeminiConsejoService("", "gemini-3.7-flash")

    with pytest.raises(ConsejoIANoDisponible):
        servicio.generar_consejo({"monto": 50000})


def test_error_de_red_se_convierte_en_consejo_no_disponible(monkeypatch):
    from google.genai import errors

    monkeypatch.setattr(
        genai,
        "Client",
        lambda **kwargs: cliente_falso(error=errors.ClientError(503, {"error": {}})),
    )

    servicio = GeminiConsejoService("clave-falsa", "gemini-3.7-flash")

    with pytest.raises(ConsejoIANoDisponible):
        servicio.generar_consejo({"monto": 50000})


def test_respuesta_vacia_se_convierte_en_consejo_no_disponible(monkeypatch):
    monkeypatch.setattr(
        genai, "Client", lambda **kwargs: cliente_falso(texto="")
    )

    servicio = GeminiConsejoService("clave-falsa", "gemini-3.7-flash")

    with pytest.raises(ConsejoIANoDisponible):
        servicio.generar_consejo({"monto": 50000})
