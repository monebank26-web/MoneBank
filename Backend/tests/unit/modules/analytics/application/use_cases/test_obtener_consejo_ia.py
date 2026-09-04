from datetime import datetime
from unittest.mock import Mock

import pytest

from app.modules.analytics.application.use_cases.obtener_consejo_ia import (
    ObtenerConsejoIA
)
from app.shared.exceptions.business_exceptions import (
    CuentaNoEncontrada,
    TransaccionesNoEncontrado,
)


def crear_fila_vista():
    fila = Mock()
    fila.id_transaccion = 7
    fila.id_usuario = 6
    fila.id_cuenta = 1
    fila.monto = 50000.50
    fila.tipo_transaccion = "GASTO"
    fila.fecha = datetime(2026, 8, 24, 12, 30)
    fila.descripcion = "Mercado"
    fila.nombre_categoria = "Supermercado"
    return fila


def crear_repository(fila):
    repository = Mock()
    repository.find_transaccion.return_value = fila
    repository.calcular_stats_mes.return_value = {
        "total_gastado_mes": 320000.75,
        "top_categorias": [
            {"nombre_categoria": "Supermercado", "total": 180000.10},
        ],
    }
    return repository


def crear_cuenta_repository(saldo=1000000.89):
    cuenta = Mock()
    cuenta.saldo = saldo
    cuenta_repository = Mock()
    cuenta_repository.get_cuenta_por_usuario.return_value = cuenta
    return cuenta_repository


def test_consejo_generado_llama_a_la_ia_y_devuelve_el_texto():
    fila = crear_fila_vista()
    repository = crear_repository(fila)
    cuenta_repository = crear_cuenta_repository()

    consejo_ia_port = Mock()
    consejo_ia_port.generar_consejo.return_value = "Buen consejo financiero."

    resultado = ObtenerConsejoIA(
        repository, cuenta_repository, consejo_ia_port
    ).execute(6, 7)

    assert resultado == "Buen consejo financiero."
    consejo_ia_port.generar_consejo.assert_called_once()


def test_contexto_enviado_a_la_ia_no_lleva_datos_personales():
    fila = crear_fila_vista()
    repository = crear_repository(fila)
    cuenta_repository = crear_cuenta_repository()
    consejo_ia_port = Mock()

    ObtenerConsejoIA(repository, cuenta_repository, consejo_ia_port).execute(6, 7)

    contexto = consejo_ia_port.generar_consejo.call_args.args[0]
    for dato_prohibido in ("id_usuario", "id_cuenta", "id_transaccion", "email"):
        assert dato_prohibido not in contexto


def test_transaccion_de_otro_usuario_lanza_no_encontrado():
    repository = Mock()
    repository.find_transaccion.return_value = None
    cuenta_repository = crear_cuenta_repository()
    consejo_ia_port = Mock()

    with pytest.raises(TransaccionesNoEncontrado):
        ObtenerConsejoIA(
            repository, cuenta_repository, consejo_ia_port
        ).execute(6, 999)

    consejo_ia_port.generar_consejo.assert_not_called()


def test_cuenta_no_encontrada_lanza_excepcion():
    repository = crear_repository(crear_fila_vista())
    cuenta_repository = Mock()
    cuenta_repository.get_cuenta_por_usuario.return_value = None
    consejo_ia_port = Mock()

    with pytest.raises(CuentaNoEncontrada):
        ObtenerConsejoIA(
            repository, cuenta_repository, consejo_ia_port
        ).execute(6, 7)

    consejo_ia_port.generar_consejo.assert_not_called()
