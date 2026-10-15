from datetime import date
from decimal import Decimal

import pytest

from app.modules.control_parental.domain.entity.mesada_parental import (
    MesadaParental,
)


def construir_mesada(**overrides):
    datos = {
        "id_mesada": 1,
        "id_control": 1,
        "id_cuenta_padre": 10,
        "id_cuenta_hijo": 20,
        "monto": Decimal("50000"),
        "frecuencia": "MENSUAL",
        "fecha_inicio": date(2026, 1, 1),
    }
    datos.update(overrides)
    return MesadaParental(**datos)


def test_validacion_creacion_ok():
    mesada = construir_mesada()

    mesada.validar_creacion(Decimal("100000"))


def test_monto_no_positivo_lanza_value_error():
    with pytest.raises(ValueError):
        construir_mesada(monto=Decimal("0")).validar_creacion(Decimal("100000"))


def test_frecuencia_invalida_lanza_value_error():
    with pytest.raises(ValueError):
        construir_mesada(frecuencia="ANUAL").validar_creacion(
            Decimal("100000")
        )


def test_fecha_fin_anterior_a_inicio_lanza_value_error():
    with pytest.raises(ValueError):
        construir_mesada(fecha_fin=date(2025, 12, 31)).validar_creacion(
            Decimal("100000")
        )


def test_saldo_insuficiente_lanza_value_error():
    with pytest.raises(ValueError):
        construir_mesada().validar_creacion(Decimal("49999"))


def test_validar_estado_ok():
    construir_mesada(estado="PAUSADA").validar_estado()


def test_estado_invalido_lanza_value_error():
    with pytest.raises(ValueError):
        construir_mesada(estado="OTRO").validar_estado()
