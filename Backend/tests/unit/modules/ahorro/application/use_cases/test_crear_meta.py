from datetime import date, timedelta
from decimal import Decimal
from unittest.mock import Mock

import pytest

from app.modules.ahorro.application.use_cases.crear_meta import CrearMeta
from app.shared.exceptions.business_exceptions import (
    CategoriaNoCompatible,
    CategoriaNoExiste,
    CuentaNoEncontrada,
    FechaObjetivoPasada,
    FechaObjetivoRequerida,
    SaldoInsuficiente,
)


def datos_validos():
    return {
        "nombre": "Viaje a San Andres",
        "monto_objetivo": Decimal("5000000.00"),
        "saldo_inicial": None,
        "fecha_objetivo": date.today() + timedelta(days=30),
        "id_categoria": 17,
    }


def repository_mock():
    repository = Mock()
    cuenta_repository = Mock()
    registrar_abono = Mock()

    cuenta = Mock()
    cuenta.id_cuenta = 1
    cuenta.saldo = Decimal("999999.00")
    repository.get_cuenta_por_usuario.return_value = cuenta

    categoria = Mock()
    categoria.tipo_categoria = "AHORRO"
    repository.get_categoria.return_value = categoria

    tipo_meta = Mock()
    tipo_meta.id_tipo_ahorro = 1
    repository.get_tipo_ahorro.return_value = tipo_meta

    return repository, cuenta_repository, registrar_abono


def test_debe_crear_una_meta_con_datos_validos():

    repository, cuenta_repository, registrar_abono = repository_mock()

    resultado = CrearMeta(repository, cuenta_repository, registrar_abono).execute(datos_validos(), 6)

    data_enviada = repository.create.call_args.args[0]
    assert data_enviada["id_cuenta"] == 1
    assert data_enviada["id_tipo_ahorro"] == 1
    assert data_enviada["estado"] == "ACTIVO"
    assert resultado == repository.create.return_value


def test_sin_cuenta_lanza_cuenta_no_encontrada():

    repository, cuenta_repository, registrar_abono = repository_mock()
    cuenta_repository.get_cuenta_por_usuario.return_value = None

    with pytest.raises(CuentaNoEncontrada):
        CrearMeta(repository, cuenta_repository, registrar_abono).execute(datos_validos(), 6)

    repository.create.assert_not_called()


def test_categoria_inexistente_lanza_categoria_no_existe():

    repository, cuenta_repository, registrar_abono = repository_mock()
    repository.get_categoria.return_value = None

    with pytest.raises(CategoriaNoExiste):
        CrearMeta(repository, cuenta_repository, registrar_abono).execute(datos_validos(), 6)

    repository.create.assert_not_called()


def test_categoria_gasto_lanza_categoria_no_compatible():

    repository, cuenta_repository, registrar_abono = repository_mock()
    repository.get_categoria.return_value.tipo_categoria = "GASTO"

    with pytest.raises(CategoriaNoCompatible):
        CrearMeta(repository, cuenta_repository, registrar_abono).execute(datos_validos(), 6)

    repository.create.assert_not_called()


def test_sin_fecha_objetivo_lanza_fecha_objetivo_requerida():

    repository, cuenta_repository, registrar_abono = repository_mock()
    datos = datos_validos()
    datos["fecha_objetivo"] = None

    with pytest.raises(FechaObjetivoRequerida):
        CrearMeta(repository, cuenta_repository, registrar_abono).execute(datos, 6)

    repository.create.assert_not_called()


def test_fecha_objetivo_pasada_lanza_fecha_objetivo_pasada():

    repository, cuenta_repository, registrar_abono = repository_mock()
    datos = datos_validos()
    datos["fecha_objetivo"] = date.today() - timedelta(days=1)

    with pytest.raises(FechaObjetivoPasada):
        CrearMeta(repository, cuenta_repository, registrar_abono).execute(datos, 6)

    repository.create.assert_not_called()


def test_saldo_inicial_mayor_al_saldo_lanza_saldo_insuficiente():

    repository, cuenta_repository, registrar_abono = repository_mock()
    datos = datos_validos()
    datos["saldo_inicial"] = Decimal("10000000.00")

    with pytest.raises(SaldoInsuficiente):
        CrearMeta(repository, cuenta_repository, registrar_abono).execute(datos, 6)

    repository.create.assert_not_called()


def test_con_saldo_inicial_registra_movimiento_de_ahorro():

    repository, cuenta_repository, registrar_abono = repository_mock()
    datos = datos_validos()
    datos["saldo_inicial"] = Decimal("50000.00")

    resultado = CrearMeta(repository, cuenta_repository, registrar_abono).execute(datos, 6)

    repository.create.assert_called_once()
    registrar_abono.execute.assert_called_once()
    datos_abono = registrar_abono.execute.call_args.args[0]
    assert datos_abono["monto"] == Decimal("50000.00")
    assert datos_abono["id_cuenta"] == 1
    assert datos_abono["id_ahorro"] == repository.create.return_value.id_ahorro
    assert datos_abono["fecha"] == date.today()
    cuenta_repository.actualizar_saldo.assert_not_called()
    assert resultado == repository.create.return_value


def test_sin_saldo_inicial_no_registra_movimiento():

    repository, cuenta_repository, registrar_abono = repository_mock()

    resultado = CrearMeta(repository, cuenta_repository, registrar_abono).execute(datos_validos(), 6)

    repository.create.assert_called_once()
    registrar_abono.execute.assert_not_called()
    cuenta_repository.actualizar_saldo.assert_not_called()
    assert resultado == repository.create.return_value
