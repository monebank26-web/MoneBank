from datetime import date
from decimal import Decimal
from unittest.mock import Mock

import pytest

from app.modules.transaccion.application.use_cases.registrar_gasto import (
    RegistrarGasto
)
from app.modules.transaccion.domain.entity.trans_entity import Transaccion
from app.shared.exceptions.business_exceptions import (
    CategoriaInvalida,
    CuentaNoEncontrada,
    CuentaNoPerteneceAlUsuario,
    FechaInvalida,
    MontoInvalido,
)


def datos_validos():
    return {
        "monto": Decimal("50000.00"),
        "fecha": date(2026, 1, 1),
        "referencia": "REF-001",
        "descripcion": "Mercado",
        "id_tipo_transaccion": 1,
        "id_cuenta": 1,
        "id_categoria": 3,
        "id_ahorro": None,
    }


def test_registrar_gasto_exitoso_guarda_y_descuenta_saldo():

    repository = Mock()

    repository.existe_categoria.return_value = True

    cuenta = Mock()
    cuenta.id_usuario = 6
    repository.get_cuenta.return_value = cuenta

    gasto_creado = {"id_transaccion": 1, "tipo": "GASTO"}
    repository.create.return_value = gasto_creado

    resultado = RegistrarGasto(repository).execute(
        datos_validos(),
        6
    )

    repository.create.assert_called_once()

    data_enviada = repository.create.call_args.args[0]
    assert data_enviada["tipo"] == Transaccion.TIPO_GASTO

    repository.descontar_saldo.assert_called_once_with(
        1,
        Decimal("50000.00")
    )

    assert resultado == gasto_creado


def test_registrar_gasto_con_monto_invalido_lanza_monto_invalido():

    repository = Mock()
    datos = datos_validos()
    datos["monto"] = Decimal("0.00")

    with pytest.raises(MontoInvalido):
        RegistrarGasto(repository).execute(
            datos,
            6
        )

    repository.create.assert_not_called()


def test_registrar_gasto_con_fecha_invalida_lanza_fecha_invalida():

    repository = Mock()
    repository.existe_categoria.return_value = True
    repository.get_cuenta.return_value = None

    datos = datos_validos()
    datos["fecha"] = "fecha-invalida"

    with pytest.raises(FechaInvalida):
        RegistrarGasto(repository).execute(
            datos,
            6
        )


def test_registrar_gasto_con_categoria_inexistente_lanza_categoria_invalida():

    repository = Mock()
    repository.existe_categoria.return_value = False

    with pytest.raises(CategoriaInvalida):
        RegistrarGasto(repository).execute(
            datos_validos(),
            6
        )

    repository.get_cuenta.assert_not_called()


def test_registrar_gasto_con_cuenta_inexistente_lanza_cuenta_no_encontrada():

    repository = Mock()
    repository.existe_categoria.return_value = True
    repository.get_cuenta.return_value = None

    with pytest.raises(CuentaNoEncontrada):
        RegistrarGasto(repository).execute(
            datos_validos(),
            6
        )

    repository.create.assert_not_called()


def test_registrar_gasto_con_cuenta_de_otro_usuario_lanza_sin_permiso():

    repository = Mock()
    repository.existe_categoria.return_value = True

    cuenta = Mock()
    cuenta.id_usuario = 99
    repository.get_cuenta.return_value = cuenta

    with pytest.raises(CuentaNoPerteneceAlUsuario):
        RegistrarGasto(repository).execute(
            datos_validos(),
            6
        )

    repository.create.assert_not_called()
    repository.descontar_saldo.assert_not_called()
