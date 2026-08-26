from unittest.mock import Mock

import httpx
import pytest

from app.modules.analytics.infrastructure.ia.gemini_consejo_service import (
    GeminiConsejoService
)
from app.shared.exceptions.business_exceptions import ConsejoIANoDisponible


def crear_respuesta_gemini(texto):
    respuesta = Mock()
    respuesta.json.return_value = {
        "candidates": [
            {
                "content": {
                    "parts": [{"text": texto}]
                }
            }
        ]
    }
    return respuesta


def test_generar_consejo_devuelve_el_texto_de_gemini(monkeypatch):
    llamadas = {}

    def post_falso(url, headers=None, json=None, timeout=None):
        llamadas["url"] = url
        llamadas["headers"] = headers
        return crear_respuesta_gemini("  Tu gasto está dentro de lo normal.  ")

    monkeypatch.setattr(httpx, "post", post_falso)

    servicio = GeminiConsejoService("clave-falsa", "gemini-2.5-flash")
    resultado = servicio.generar_consejo({"monto": 50000})

    assert resultado == "Tu gasto está dentro de lo normal."
    assert "gemini-2.5-flash:generateContent" in llamadas["url"]
    assert llamadas["headers"]["x-goog-api-key"] == "clave-falsa"


def test_generar_consejo_sin_api_key_falla_sin_llamar_red(monkeypatch):
    def post_falso(*args, **kwargs):
        raise AssertionError("No debe llamar a la red sin api key")

    monkeypatch.setattr(httpx, "post", post_falso)

    servicio = GeminiConsejoService("", "gemini-2.5-flash")

    with pytest.raises(ConsejoIANoDisponible):
        servicio.generar_consejo({"monto": 50000})


def test_error_de_red_se_convierte_en_consejo_no_disponible(monkeypatch):
    def post_falso(*args, **kwargs):
        raise httpx.ConnectError("sin conexión")

    monkeypatch.setattr(httpx, "post", post_falso)

    servicio = GeminiConsejoService("clave-falsa", "gemini-2.5-flash")

    with pytest.raises(ConsejoIANoDisponible):
        servicio.generar_consejo({"monto": 50000})


def test_respuesta_vacia_se_convierte_en_consejo_no_disponible(monkeypatch):
    respuesta = Mock()
    respuesta.json.return_value = {"candidates": []}

    def post_falso(*args, **kwargs):
        return respuesta

    monkeypatch.setattr(httpx, "post", post_falso)

    servicio = GeminiConsejoService("clave-falsa", "gemini-2.5-flash")

    with pytest.raises(ConsejoIANoDisponible):
        servicio.generar_consejo({"monto": 50000})
