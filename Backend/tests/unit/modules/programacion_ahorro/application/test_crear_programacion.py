from datetime import date
from decimal import Decimal
from unittest.mock import Mock

import pytest

from app.modules.programacion_ahorro.application.crear_programacion import CrearProgramacion
from app.shared.exceptions.ahorro_errors import (
    AhorroNoEncontrado,
    FechaCobroInvalida,
    FrecuenciaInvalida,
    ProgramacionDuplicada,
    RangoFechasInvalido,
)
from app.shared.exceptions.transaccion_errors import (
    AhorroAsociadoNoValido,
    CuentaNoEncontrada,
    CuentaNoPerteneceAlUsuario,
)


@pytest.fixture(autouse=True)
def hoy_fijo(monkeypatch):
    monkeypatch.setattr(
        "app.shared.utils.fechas.hoy_colombia",
        lambda: date(2026, 8, 1),
    )


def datos_validos():
    return {
        "id_ahorro": 47,
        "monto_periodico": Decimal("50000.00"),
        "fecha_cobro": date(2026, 9, 1),
        "frecuencia": "MENSUAL",
        "fecha_fin": date(2027, 9, 1),
    }


def mocks_con_cuenta():
    repository = Mock()
    repository.obtener_por_ahorro.return_value = None

    cuenta = Mock()
    cuenta.id_cuenta = 1
    cuenta_repository = Mock()
    cuenta_repository.get_cuenta_por_usuario.return_value = cuenta

    ahorro = Mock()
    ahorro.id_ahorro = 47
    ahorro.id_cuenta = 1
    ahorro.id_tipo_ahorro = 1
    ahorro_repository = Mock()
    ahorro_repository.get_by_id.return_value = ahorro

    tipo_limite = Mock()
    tipo_limite.id_tipo_ahorro = 3
    ahorro_repository.get_tipo_ahorro.return_value = tipo_limite

    creada = Mock()
    creada.id_programacion_ahorro = 1
    repository.create.return_value = creada

    return repository, cuenta_repository, ahorro_repository


def test_debe_crear_una_programacion_valida():

    repository, cuenta_repository, ahorro_repository = mocks_con_cuenta()

    resultado = CrearProgramacion(
        repository, cuenta_repository, ahorro_repository
    ).execute(datos_validos(), 6)

    data_enviada = repository.create.call_args.args[0]
    assert data_enviada["id_ahorro"] == 47
    assert data_enviada["monto_periodico"] == Decimal("50000.00")
    assert data_enviada["fecha_cobro"] == date(2026, 9, 1)
    assert data_enviada["frecuencia"] == "MENSUAL"
    assert data_enviada["fecha_inicio"] == date(2026, 9, 1)
    assert data_enviada["fecha_fin"] == date(2027, 9, 1)
    assert data_enviada["estado"] == "ACTIVA"

    cuenta_repository.get_cuenta_por_usuario.assert_called_once_with(6)
    ahorro_repository.get_by_id.assert_called_once_with(47)
    ahorro_repository.get_tipo_ahorro.assert_called_once()
    repository.obtener_por_ahorro.assert_called_once_with(47)
    assert resultado == repository.create.return_value


def test_sin_cuenta_lanza_cuenta_no_encontrada():

    repository, cuenta_repository, ahorro_repository = mocks_con_cuenta()
    cuenta_repository.get_cuenta_por_usuario.return_value = None

    with pytest.raises(CuentaNoEncontrada):
        CrearProgramacion(
            repository, cuenta_repository, ahorro_repository
        ).execute(datos_validos(), 6)

    repository.create.assert_not_called()


def test_con_ahorro_inexistente_lanza_ahorro_no_encontrado():

    repository, cuenta_repository, ahorro_repository = mocks_con_cuenta()
    ahorro_repository.get_by_id.return_value = None

    with pytest.raises(AhorroNoEncontrado):
        CrearProgramacion(
            repository, cuenta_repository, ahorro_repository
        ).execute(datos_validos(), 6)

    repository.create.assert_not_called()


def test_con_ahorro_de_otra_cuenta_lanza_cuenta_no_pertenece_al_usuario():

    repository, cuenta_repository, ahorro_repository = mocks_con_cuenta()
    ahorro_repository.get_by_id.return_value.id_cuenta = 99

    with pytest.raises(CuentaNoPerteneceAlUsuario):
        CrearProgramacion(
            repository, cuenta_repository, ahorro_repository
        ).execute(datos_validos(), 6)

    repository.create.assert_not_called()


def test_con_ahorro_tipo_limite_lanza_ahorro_asociado_no_valido():

    repository, cuenta_repository, ahorro_repository = mocks_con_cuenta()
    ahorro_repository.get_by_id.return_value.id_tipo_ahorro = 3

    with pytest.raises(AhorroAsociadoNoValido):
        CrearProgramacion(
            repository, cuenta_repository, ahorro_repository
        ).execute(datos_validos(), 6)

    repository.create.assert_not_called()


def test_frecuencia_invalida_lanza_frecuencia_invalida():

    repository, cuenta_repository, ahorro_repository = mocks_con_cuenta()
    datos = datos_validos()
    datos["frecuencia"] = "CADA_VEZ"

    with pytest.raises(FrecuenciaInvalida):
        CrearProgramacion(
            repository, cuenta_repository, ahorro_repository
        ).execute(datos, 6)

    repository.create.assert_not_called()


def test_fecha_cobro_no_posterior_a_hoy_lanza_fecha_cobro_invalida():

    repository, cuenta_repository, ahorro_repository = mocks_con_cuenta()
    datos = datos_validos()
    datos["fecha_cobro"] = date(2026, 8, 1)

    with pytest.raises(FechaCobroInvalida):
        CrearProgramacion(
            repository, cuenta_repository, ahorro_repository
        ).execute(datos, 6)

    repository.create.assert_not_called()


def test_fecha_fin_anterior_a_cobro_lanza_rango_invalido():

    repository, cuenta_repository, ahorro_repository = mocks_con_cuenta()
    datos = datos_validos()
    datos["fecha_fin"] = date(2026, 8, 1)

    with pytest.raises(RangoFechasInvalido):
        CrearProgramacion(
            repository, cuenta_repository, ahorro_repository
        ).execute(datos, 6)

    repository.create.assert_not_called()


def test_sin_fecha_fin_es_valido():

    repository, cuenta_repository, ahorro_repository = mocks_con_cuenta()
    datos = datos_validos()
    datos["fecha_fin"] = None

    resultado = CrearProgramacion(
        repository, cuenta_repository, ahorro_repository
    ).execute(datos, 6)

    data_enviada = repository.create.call_args.args[0]
    assert data_enviada["fecha_fin"] is None
    assert resultado == repository.create.return_value


def test_programacion_duplicada_lanza_programacion_duplicada():

    repository, cuenta_repository, ahorro_repository = mocks_con_cuenta()
    repository.obtener_por_ahorro.return_value = Mock()

    with pytest.raises(ProgramacionDuplicada):
        CrearProgramacion(
            repository, cuenta_repository, ahorro_repository
        ).execute(datos_validos(), 6)

    repository.create.assert_not_called()