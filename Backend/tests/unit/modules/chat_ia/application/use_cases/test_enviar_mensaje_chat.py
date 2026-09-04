from unittest.mock import Mock

import pytest

from app.modules.chat_ia.application.use_cases.enviar_mensaje_chat import (
    EnviarMensajeChat
)
from app.shared.exceptions.business_exceptions import CuentaNoEncontrada


def crear_cuenta():
    cuenta = Mock()
    cuenta.id_cuenta = 1
    cuenta.saldo = 1000000.50
    return cuenta


def crear_repos():
    cuenta_repo = Mock()
    cuenta_repo.get_cuenta_por_usuario.return_value = crear_cuenta()

    ahorro_repo = Mock()
    ahorro_repo.get_metas_activas.return_value = [
        {
            "nombre": "Viaje",
            "monto_objetivo": 3000000,
            "saldo_actual": 1200000,
        }
    ]
    ahorro_repo.get_by_cuenta_y_tipo.return_value = [
        Mock(nombre="Alimentación", monto_objetivo=500000, periodo="MENSUAL")
    ]

    transacc_repo = Mock()
    transacc_repo.sumar_ingresos.return_value = 2000000.20
    transacc_repo.sumar_gastos.return_value = 800000.80
    transacc_repo.top_categorias.return_value = [
        {"nombre_categoria": "Supermercado", "total": 180000.60}
    ]

    return cuenta_repo, ahorro_repo, transacc_repo


def test_execute_devuelve_respuesta_del_port():
    cuenta_repo, ahorro_repo, transacc_repo = crear_repos()
    chat_ia = Mock()
    chat_ia.generar_respuesta.return_value = "Buen consejo."

    resultado = EnviarMensajeChat(
        cuenta_repo, ahorro_repo, transacc_repo, chat_ia
    ).execute(6, "¿cómo voy?", [{"rol": "user", "texto": "hola"}])

    assert resultado == "Buen consejo."
    chat_ia.generar_respuesta.assert_called_once()


def test_arma_contexto_con_los_tres_repos():
    cuenta_repo, ahorro_repo, transacc_repo = crear_repos()
    chat_ia = Mock()
    chat_ia.generar_respuesta.return_value = "ok"

    EnviarMensajeChat(
        cuenta_repo, ahorro_repo, transacc_repo, chat_ia
    ).execute(6, "m", [])

    contexto = chat_ia.generar_respuesta.call_args.args[0]
    assert contexto["saldo_actual"] == 1000000
    assert contexto["ingreso_mes"] == 2000000
    assert contexto["gasto_mes"] == 800001
    assert "top_categorias" in contexto
    assert "metas_ahorro" in contexto
    assert "limites_activos" in contexto
    assert contexto["metas_ahorro"][0]["nombre"] == "Viaje"
    assert contexto["limites_activos"][0]["nombre"] == "Alimentación"


def test_contexto_no_lleva_datos_personales():
    cuenta_repo, ahorro_repo, transacc_repo = crear_repos()
    chat_ia = Mock()
    chat_ia.generar_respuesta.return_value = "ok"

    EnviarMensajeChat(
        cuenta_repo, ahorro_repo, transacc_repo, chat_ia
    ).execute(6, "m", [])

    contexto = chat_ia.generar_respuesta.call_args.args[0]
    for dato_prohibido in ("id_usuario", "id_cuenta", "email"):
        assert dato_prohibido not in contexto


def test_sin_cuenta_lanza_cuenta_no_encontrada():
    cuenta_repo = Mock()
    cuenta_repo.get_cuenta_por_usuario.return_value = None
    chat_ia = Mock()

    with pytest.raises(CuentaNoEncontrada):
        EnviarMensajeChat(
            cuenta_repo, Mock(), Mock(), chat_ia
        ).execute(6, "m", [])

    chat_ia.generar_respuesta.assert_not_called()
