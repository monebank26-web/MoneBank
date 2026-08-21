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

    cuenta = Mock()
    cuenta.id_cuenta = 1
    repository.get_cuenta_por_usuario.return_value = cuenta

    categoria = Mock()
    categoria.tipo_categoria = "AHORRO"
    repository.get_categoria.return_value = categoria

    tipo_meta = Mock()
    tipo_meta.id_tipo_ahorro = 1
    repository.get_tipo_ahorro.return_value = tipo_meta

    return repository


def test_debe_crear_una_meta_con_datos_validos():

    repository = repository_mock()

    resultado = CrearMeta(repository).execute(datos_validos(), 6)

    data_enviada = repository.create.call_args.args[0]
    assert data_enviada["id_cuenta"] == 1
    assert data_enviada["id_tipo_ahorro"] == 1
    assert data_enviada["estado"] == "ACTIVO"
    assert resultado == repository.create.return_value


def test_sin_cuenta_lanza_cuenta_no_encontrada():

    repository = repository_mock()
    repository.get_cuenta_por_usuario.return_value = None

    with pytest.raises(CuentaNoEncontrada):
        CrearMeta(repository).execute(datos_validos(), 6)

    repository.create.assert_not_called()


def test_categoria_inexistente_lanza_categoria_no_existe():

    repository = repository_mock()
    repository.get_categoria.return_value = None

    with pytest.raises(CategoriaNoExiste):
        CrearMeta(repository).execute(datos_validos(), 6)

    repository.create.assert_not_called()


def test_categoria_gasto_lanza_categoria_no_compatible():

    repository = repository_mock()
    repository.get_categoria.return_value.tipo_categoria = "GASTO"

    with pytest.raises(CategoriaNoCompatible):
        CrearMeta(repository).execute(datos_validos(), 6)

    repository.create.assert_not_called()


def test_sin_fecha_objetivo_lanza_fecha_objetivo_requerida():

    repository = repository_mock()
    datos = datos_validos()
    datos["fecha_objetivo"] = None

    with pytest.raises(FechaObjetivoRequerida):
        CrearMeta(repository).execute(datos, 6)

    repository.create.assert_not_called()


def test_fecha_objetivo_pasada_lanza_fecha_objetivo_pasada():

    repository = repository_mock()
    datos = datos_validos()
    datos["fecha_objetivo"] = date.today() - timedelta(days=1)

    with pytest.raises(FechaObjetivoPasada):
        CrearMeta(repository).execute(datos, 6)

    repository.create.assert_not_called()
