from datetime import date
from decimal import Decimal
from unittest.mock import Mock

import pytest

from app.modules.programacion_ahorro.application.crear_programacion import CrearProgramacion
from app.shared.exceptions.business_exceptions import (
    CuentaNoEncontrada,
    FrecuenciaInvalida,
    RangoFechasInvalido,
)


def datos_validos():
    return {
        "monto_periodico": Decimal("50000.00"),
        "fecha_cobro": date(2026, 9, 1),
        "frecuencia": "MENSUAL",
        "fecha_inicio": date(2026, 9, 1),
        "fecha_fin": date(2027, 9, 1),
    }


def mocks_con_cuenta():
    repository = Mock()
    cuenta_repository = Mock()

    cuenta = Mock()
    cuenta.id_cuenta = 1
    cuenta_repository.get_cuenta_por_usuario.return_value = cuenta

    creada = Mock()
    creada.id_programacion_ahorro = 1
    repository.create.return_value = creada

    return repository, cuenta_repository


def test_debe_crear_una_programacion_valida():

    repository, cuenta_repository = mocks_con_cuenta()

    resultado = CrearProgramacion(repository, cuenta_repository).execute(
        datos_validos(), 6
    )

    data_enviada = repository.create.call_args.args[0]
    assert data_enviada["monto_periodico"] == Decimal("50000.00")
    assert data_enviada["fecha_cobro"] == date(2026, 9, 1)
    assert data_enviada["frecuencia"] == "MENSUAL"
    assert data_enviada["fecha_inicio"] == date(2026, 9, 1)
    assert data_enviada["fecha_fin"] == date(2027, 9, 1)
    assert data_enviada["estado"] == "ACTIVA"

    cuenta_repository.get_cuenta_por_usuario.assert_called_once_with(6)
    assert resultado == repository.create.return_value


def test_sin_cuenta_lanza_cuenta_no_encontrada():

    repository, cuenta_repository = mocks_con_cuenta()
    cuenta_repository.get_cuenta_por_usuario.return_value = None

    with pytest.raises(CuentaNoEncontrada):
        CrearProgramacion(repository, cuenta_repository).execute(datos_validos(), 6)

    repository.create.assert_not_called()


def test_frecuencia_invalida_lanza_frecuencia_invalida():

    repository, cuenta_repository = mocks_con_cuenta()
    datos = datos_validos()
    datos["frecuencia"] = "CADA_VEZ"

    with pytest.raises(FrecuenciaInvalida):
        CrearProgramacion(repository, cuenta_repository).execute(datos, 6)

    repository.create.assert_not_called()


def test_fecha_fin_anterior_a_inicio_lanza_rango_invalido():

    repository, cuenta_repository = mocks_con_cuenta()
    datos = datos_validos()
    datos["fecha_inicio"] = date(2027, 1, 1)
    datos["fecha_fin"] = date(2026, 1, 1)

    with pytest.raises(RangoFechasInvalido):
        CrearProgramacion(repository, cuenta_repository).execute(datos, 6)

    repository.create.assert_not_called()


def test_sin_fecha_fin_es_valido():

    repository, cuenta_repository = mocks_con_cuenta()
    datos = datos_validos()
    datos["fecha_fin"] = None

    resultado = CrearProgramacion(repository, cuenta_repository).execute(datos, 6)

    data_enviada = repository.create.call_args.args[0]
    assert data_enviada["fecha_fin"] is None
    assert resultado == repository.create.return_value