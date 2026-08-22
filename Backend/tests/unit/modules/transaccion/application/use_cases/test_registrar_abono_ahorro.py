from datetime import date
from decimal import Decimal
from unittest.mock import Mock

import pytest

from app.modules.transaccion.application.use_cases.registrar_abono_ahorro import (
    RegistrarAbonoAhorro
)
from app.shared.exceptions.business_exceptions import (
    AhorroAsociadoNoValido,
    CuentaNoEncontrada,
    CuentaNoPerteneceAlUsuario,
    SaldoInsuficiente,
    TipoTransaccionNoValido,
)


def datos_validos():
    return {
        "monto": Decimal("20000.00"),
        "fecha": date(2026, 1, 15),
        "descripcion": "Abono a meta",
        "id_cuenta": 1,
        "id_ahorro": 47,
    }


def repository_base():
    repository = Mock()

    cuenta = Mock()
    cuenta.id_usuario = 6
    cuenta.id_cuenta = 1
    cuenta.saldo = Decimal("98250.00")
    repository.get_cuenta.return_value = cuenta

    ahorro = Mock()
    ahorro.id_ahorro = 47
    ahorro.id_cuenta = 1
    ahorro.id_tipo_ahorro = 1
    ahorro.id_categoria = 17
    repository.get_ahorro.return_value = ahorro

    tipo_limite = Mock()
    tipo_limite.id_tipo_ahorro = 3
    repository.get_tipo_ahorro.return_value = tipo_limite

    tipo_movimiento = Mock()
    tipo_movimiento.id_tipo_transaccion = 3
    repository.get_tipo_transaccion.return_value = tipo_movimiento

    return repository


def test_registrar_abono_exitoso_inserta_y_no_descuenta_saldo():

    repository = repository_base()

    abono_creado = {"id_transaccion": 99, "id_tipo_transaccion": 3}
    repository.create.return_value = abono_creado

    resultado = RegistrarAbonoAhorro(repository).execute(
        datos_validos(),
        6
    )

    repository.create.assert_called_once()

    data_enviada = repository.create.call_args.args[0]
    assert data_enviada["id_tipo_transaccion"] == 3
    assert data_enviada["id_cuenta"] == 1
    assert data_enviada["id_ahorro"] == 47
    assert data_enviada["id_categoria"] == 17

    repository.descontar_saldo.assert_not_called()

    assert resultado == abono_creado


def test_registrar_abono_sin_tipo_en_catalogo_lanza_error():

    repository = repository_base()
    repository.get_tipo_transaccion.return_value = None

    with pytest.raises(TipoTransaccionNoValido):
        RegistrarAbonoAhorro(repository).execute(datos_validos(), 6)

    repository.create.assert_not_called()


def test_registrar_abono_con_cuenta_inexistente_lanza_error():

    repository = repository_base()
    repository.get_cuenta.return_value = None

    with pytest.raises(CuentaNoEncontrada):
        RegistrarAbonoAhorro(repository).execute(datos_validos(), 6)

    repository.create.assert_not_called()


def test_registrar_abono_con_cuenta_de_otro_lanza_error():

    repository = repository_base()
    repository.get_cuenta.return_value.id_usuario = 99

    with pytest.raises(CuentaNoPerteneceAlUsuario):
        RegistrarAbonoAhorro(repository).execute(datos_validos(), 6)

    repository.create.assert_not_called()


def test_registrar_abono_con_ahorro_inexistente_lanza_error():

    repository = repository_base()
    repository.get_ahorro.return_value = None

    with pytest.raises(AhorroAsociadoNoValido):
        RegistrarAbonoAhorro(repository).execute(datos_validos(), 6)

    repository.create.assert_not_called()


def test_registrar_abono_con_ahorro_de_otra_cuenta_lanza_error():

    repository = repository_base()
    repository.get_ahorro.return_value.id_cuenta = 99

    with pytest.raises(AhorroAsociadoNoValido):
        RegistrarAbonoAhorro(repository).execute(datos_validos(), 6)

    repository.create.assert_not_called()


def test_registrar_abono_a_un_limite_lanza_error():

    repository = repository_base()
    repository.get_ahorro.return_value.id_tipo_ahorro = 3

    with pytest.raises(AhorroAsociadoNoValido):
        RegistrarAbonoAhorro(repository).execute(datos_validos(), 6)

    repository.create.assert_not_called()


def test_registrar_abono_sin_fondos_lanza_error():

    repository = repository_base()
    repository.get_cuenta.return_value.saldo = Decimal("100.00")

    with pytest.raises(SaldoInsuficiente):
        RegistrarAbonoAhorro(repository).execute(datos_validos(), 6)

    repository.create.assert_not_called()
    repository.descontar_saldo.assert_not_called()
