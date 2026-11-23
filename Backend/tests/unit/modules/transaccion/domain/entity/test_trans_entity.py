from datetime import date, datetime

import pytest

from app.modules.transaccion.domain.entity.trans_entity import Transaccion
from app.shared.exceptions.common import MontoInvalido
from app.shared.exceptions.transaccion_errors import (
    FechaInvalida,
    TipoTransaccionNoValido,
)


def construir_transaccion(**overrides):
    datos = {
        "id": None,
        "monto": 15000,
        "tipo": Transaccion.TIPO_GASTO,
        "fecha": datetime(2026, 10, 1, 10, 0, 0),
        "descripcion": "mercado",
        "categoria": 5,
    }
    datos.update(overrides)
    return Transaccion(**datos)


def test_construye_transaccion_valida():
    transaccion = construir_transaccion()

    assert transaccion.monto == 15000
    assert transaccion.tipo == Transaccion.TIPO_GASTO
    assert transaccion.es_gasto() is True
    assert transaccion.es_ingreso() is False


def test_tipo_invalido_lanza_tipo_transaccion_no_valido():
    with pytest.raises(TipoTransaccionNoValido):
        construir_transaccion(tipo="OTRO")


def test_monto_no_positivo_lanza_monto_invalido():
    with pytest.raises(MontoInvalido):
        construir_transaccion(monto=0)

    with pytest.raises(MontoInvalido):
        construir_transaccion(monto=-100)

    with pytest.raises(MontoInvalido):
        construir_transaccion(monto=None)


def test_fecha_invalida_lanza_fecha_invalida():
    with pytest.raises(FechaInvalida):
        construir_transaccion(fecha="2026-10-01")


def test_acepta_date_ademas_de_datetime():
    transaccion = construir_transaccion(fecha=date(2026, 10, 1))

    assert transaccion.fecha == date(2026, 10, 1)


def test_predicados_de_tipo():
    ingreso = construir_transaccion(tipo=Transaccion.TIPO_INGRESO)
    ahorro = construir_transaccion(tipo=Transaccion.TIPO_AHORRO)
    movimiento = construir_transaccion(
        tipo=Transaccion.TIPO_MOVIMIENTO_AHORRO
    )

    assert ingreso.es_ingreso() is True
    assert ahorro.es_ahorro() is True
    assert movimiento.es_movimiento_ahorro() is True
