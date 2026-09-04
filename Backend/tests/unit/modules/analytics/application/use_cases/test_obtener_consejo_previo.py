from unittest.mock import Mock

import pytest

from app.modules.analytics.application.use_cases.obtener_consejo_previo import (
    ObtenerConsejoPrevio,
)
from app.shared.exceptions.business_exceptions import (
    CategoriaInvalida,
    CuentaNoEncontrada,
)


def crear_repository_con_datos():
    repository = Mock()
    repository.get_categoria_nombre.return_value = "Alimentación"
    repository.calcular_stats_mes.return_value = {
        "total_gastado_mes": 450000,
        "top_categorias": [
            {"nombre_categoria": "Alimentación", "total": 180000},
        ],
    }
    repository.get_resumen_categoria.return_value = {
        "gasto_mes": 180000,
        "gasto_mes_anterior": 220000,
        "promedio_3_meses": 200000,
        "num_transacciones_mes": 8,
        "num_transacciones_mes_anterior": 5,
        "transacciones_recientes": [
            {"monto": 25000, "fecha": "hace 2 días"},
            {"monto": 35000, "fecha": "hace 5 días"},
        ],
    }
    repository.get_limite_categoria.return_value = {
        "monto_limite": 300000,
        "gasto_actual": 180000,
        "periodo": "MENSUAL",
    }
    return repository


def crear_cuenta_repository(saldo=250000):
    cuenta_repository = Mock()
    cuenta_repository.get_cuenta_por_usuario.return_value = Mock(saldo=saldo)
    return cuenta_repository


def test_consejo_previo_generado_devuelve_el_texto():
    repository = crear_repository_con_datos()
    cuenta_repository = crear_cuenta_repository()
    consejo_ia_port = Mock()
    consejo_ia_port.generar_consejo.return_value = "Consejo previo financiero."

    resultado = ObtenerConsejoPrevio(
        repository, cuenta_repository, consejo_ia_port
    ).execute(6, 50000, 3)

    assert resultado == "Consejo previo financiero."
    consejo_ia_port.generar_consejo.assert_called_once()


def test_consejo_previo_llama_a_la_ia_con_es_previo_true():
    repository = crear_repository_con_datos()
    cuenta_repository = crear_cuenta_repository()
    consejo_ia_port = Mock()
    consejo_ia_port.generar_consejo.return_value = "Consejo."

    ObtenerConsejoPrevio(
        repository, cuenta_repository, consejo_ia_port
    ).execute(6, 50000, 3)

    llamada = consejo_ia_port.generar_consejo.call_args
    assert llamada.kwargs.get("es_previo") is True


def test_contexto_incluye_historial_categoria():
    repository = crear_repository_con_datos()
    cuenta_repository = crear_cuenta_repository()
    consejo_ia_port = Mock()
    consejo_ia_port.generar_consejo.return_value = "Consejo."

    ObtenerConsejoPrevio(
        repository, cuenta_repository, consejo_ia_port
    ).execute(6, 50000, 3)

    contexto = consejo_ia_port.generar_consejo.call_args.args[0]
    historial = contexto["historial_categoria"]
    assert historial["gasto_actual_mes"] == 180000
    assert historial["gasto_mes_anterior"] == 220000
    assert historial["promedio_3_meses"] == 200000
    assert historial["numero_transacciones_mes"] == 8
    assert historial["numero_transacciones_mes_anterior"] == 5
    assert len(historial["transacciones_recientes"]) == 2


def test_contexto_incluye_limite_con_porcentajes():
    repository = crear_repository_con_datos()
    cuenta_repository = crear_cuenta_repository()
    consejo_ia_port = Mock()
    consejo_ia_port.generar_consejo.return_value = "Consejo."

    ObtenerConsejoPrevio(
        repository, cuenta_repository, consejo_ia_port
    ).execute(6, 50000, 3)

    contexto = consejo_ia_port.generar_consejo.call_args.args[0]
    assert "limite" in contexto
    assert contexto["limite"]["monto_limite"] == 300000
    assert contexto["limite"]["porcentaje_usado"] == 60
    assert contexto["limite"]["porcentaje_proyectado"] == 77


def test_contexto_sin_limite_cuando_no_existe():
    repository = crear_repository_con_datos()
    repository.get_limite_categoria.return_value = None
    cuenta_repository = crear_cuenta_repository()
    consejo_ia_port = Mock()
    consejo_ia_port.generar_consejo.return_value = "Consejo."

    ObtenerConsejoPrevio(
        repository, cuenta_repository, consejo_ia_port
    ).execute(6, 50000, 3)

    contexto = consejo_ia_port.generar_consejo.call_args.args[0]
    assert "limite" not in contexto


def test_contexto_no_lleva_datos_personales():
    repository = crear_repository_con_datos()
    cuenta_repository = crear_cuenta_repository()
    consejo_ia_port = Mock()
    consejo_ia_port.generar_consejo.return_value = "Consejo."

    ObtenerConsejoPrevio(
        repository, cuenta_repository, consejo_ia_port
    ).execute(6, 50000, 3)

    contexto = consejo_ia_port.generar_consejo.call_args.args[0]
    for dato_prohibido in ("id_usuario", "id_cuenta", "id_transaccion", "email"):
        assert dato_prohibido not in contexto


def test_cuenta_no_encontrada_lanza_excepcion():
    repository = Mock()
    cuenta_repository = Mock()
    cuenta_repository.get_cuenta_por_usuario.return_value = None
    consejo_ia_port = Mock()

    with pytest.raises(CuentaNoEncontrada):
        ObtenerConsejoPrevio(
            repository, cuenta_repository, consejo_ia_port
        ).execute(6, 50000, 3)

    consejo_ia_port.generar_consejo.assert_not_called()


def test_categoria_invalida_lanza_excepcion():
    repository = Mock()
    repository.get_categoria_nombre.return_value = None
    cuenta_repository = crear_cuenta_repository()
    consejo_ia_port = Mock()

    with pytest.raises(CategoriaInvalida):
        ObtenerConsejoPrevio(
            repository, cuenta_repository, consejo_ia_port
        ).execute(6, 50000, 999)

    consejo_ia_port.generar_consejo.assert_not_called()
