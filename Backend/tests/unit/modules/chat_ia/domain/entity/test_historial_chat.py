import pytest

from app.modules.chat_ia.domain.entity.historial_chat import HistorialChat
from app.shared.exceptions.business_exceptions import ChatInvalido


def turnos_wire(n):
    return [
        {"rol": ("user" if i % 2 == 0 else "model"), "texto": str(i)}
        for i in range(n)
    ]


def test_rol_invalido_lanza_chat_invalido():
    with pytest.raises(ChatInvalido):
        HistorialChat([{"rol": "admin", "texto": "hola"}])


def test_texto_no_str_lanza_chat_invalido():
    with pytest.raises(ChatInvalido):
        HistorialChat([{"rol": "user", "texto": 123}])


def test_no_es_lista_lanza_chat_invalido():
    with pytest.raises(ChatInvalido):
        HistorialChat("no-soy-lista")


def test_muchos_turnos_trunca_a_doce():
    historial = HistorialChat(turnos_wire(15))
    assert len(historial.contenido_gemini) == 12


def test_contenido_gemini_formato_correcto():
    historial = HistorialChat([{"rol": "user", "texto": "hola"}])
    assert historial.contenido_gemini == [
        {"role": "user", "parts": [{"text": "hola"}]}
    ]


def test_agregar_anade_y_convierte_a_role_parts():
    historial = HistorialChat([])
    resultado = historial.agregar({"rol": "user", "texto": "cuánto gasté"})
    assert resultado[-1] == {
        "role": "user",
        "parts": [{"text": "cuánto gasté"}],
    }


def test_agregar_mantiene_limite_de_doce():
    historial = HistorialChat(turnos_wire(11))
    historial.agregar({"rol": "user", "texto": "nuevo"})
    assert len(historial.contenido_gemini) == 12
