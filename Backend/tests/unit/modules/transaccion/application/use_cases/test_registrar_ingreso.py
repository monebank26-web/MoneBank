from datetime import date
from decimal import Decimal
from unittest.mock import Mock

import pytest

from app.modules.transaccion.application.use_cases.registrar_ingreso import (
    RegistrarIngreso
)
from app.shared.exceptions.business_exceptions import (
    AhorroAsociadoNoValido,
    CategoriaInvalida,
    CuentaNoEncontrada,
    CuentaNoPerteneceAlUsuario,
    FechaInvalida,
    MontoInvalido,
    TipoTransaccionNoValido,
)


def datos_validos():
    return {
        "monto": Decimal("50000.00"),
        "fecha": date(2026, 1, 1),
        "descripcion": "Salario",
        "id_tipo_transaccion": 1,
        "id_cuenta": 1,
        "id_categoria": 3,
        "id_ahorro": None,
    }


def test_registrar_ingreso_exitoso_guarda_y_aumenta_saldo():

    repository = Mock()

    repository.existe_categoria.return_value = True

    cuenta = Mock()
    cuenta.id_usuario = 6
    cuenta.saldo = Decimal("100000.00")
    repository.get_cuenta.return_value = cuenta

    tipo_ingreso = Mock()
    tipo_ingreso.id_tipo_transaccion = 1
    repository.get_tipo_transaccion.return_value = tipo_ingreso

    ingreso_creado = {"id_transaccion": 1, "id_tipo_transaccion": 1}
    repository.create.return_value = ingreso_creado

    resultado = RegistrarIngreso(repository).execute(
        datos_validos(),
        6
    )

    repository.create.assert_called_once()

    data_enviada = repository.create.call_args.args[0]
    assert data_enviada["id_tipo_transaccion"] == 1

    repository.aumentar_saldo.assert_called_once_with(
        1,
        Decimal("50000.00")
    )

    assert resultado == ingreso_creado


def test_registrar_ingreso_con_ahorro_valido_asocia_el_id():

    repository = Mock()

    repository.existe_categoria.return_value = True

    cuenta = Mock()
    cuenta.id_usuario = 6
    cuenta.id_cuenta = 1
    cuenta.saldo = Decimal("100000.00")
    repository.get_cuenta.return_value = cuenta

    tipo_ingreso = Mock()
    tipo_ingreso.id_tipo_transaccion = 1
    repository.get_tipo_transaccion.return_value = tipo_ingreso

    ahorro = Mock()
    ahorro.id_cuenta = 1
    repository.get_ahorro.return_value = ahorro

    datos = datos_validos()
    datos["id_ahorro"] = 46

    RegistrarIngreso(repository).execute(datos, 6)

    data_enviada = repository.create.call_args.args[0]
    assert data_enviada["id_ahorro"] == 46


def test_registrar_ingreso_con_ahorro_inexistente_lanza_error():

    repository = Mock()

    repository.existe_categoria.return_value = True

    cuenta = Mock()
    cuenta.id_usuario = 6
    cuenta.id_cuenta = 1
    cuenta.saldo = Decimal("100000.00")
    repository.get_cuenta.return_value = cuenta

    tipo_ingreso = Mock()
    repository.get_tipo_transaccion.return_value = tipo_ingreso

    repository.get_ahorro.return_value = None

    datos = datos_validos()
    datos["id_ahorro"] = 999

    with pytest.raises(AhorroAsociadoNoValido):
        RegistrarIngreso(repository).execute(datos, 6)

    repository.create.assert_not_called()


def test_registrar_ingreso_con_ahorro_de_otra_cuenta_lanza_error():

    repository = Mock()

    repository.existe_categoria.return_value = True

    cuenta = Mock()
    cuenta.id_usuario = 6
    cuenta.id_cuenta = 1
    cuenta.saldo = Decimal("100000.00")
    repository.get_cuenta.return_value = cuenta

    tipo_ingreso = Mock()
    repository.get_tipo_transaccion.return_value = tipo_ingreso

    ahorro = Mock()
    ahorro.id_cuenta = 99
    repository.get_ahorro.return_value = ahorro

    datos = datos_validos()
    datos["id_ahorro"] = 46

    with pytest.raises(AhorroAsociadoNoValido):
        RegistrarIngreso(repository).execute(datos, 6)

    repository.create.assert_not_called()


def test_registrar_ingreso_sin_ahorro_envia_none():

    repository = Mock()

    repository.existe_categoria.return_value = True

    cuenta = Mock()
    cuenta.id_usuario = 6
    cuenta.id_cuenta = 1
    cuenta.saldo = Decimal("100000.00")
    repository.get_cuenta.return_value = cuenta

    tipo_ingreso = Mock()
    tipo_ingreso.id_tipo_transaccion = 1
    repository.get_tipo_transaccion.return_value = tipo_ingreso

    repository.get_ahorro.assert_not_called()

    datos = datos_validos()
    datos["id_ahorro"] = None

    RegistrarIngreso(repository).execute(datos, 6)

    data_enviada = repository.create.call_args.args[0]
    assert data_enviada["id_ahorro"] is None


def test_registrar_ingreso_con_monto_invalido_lanza_monto_invalido():

    repository = Mock()
    datos = datos_validos()
    datos["monto"] = Decimal("0.00")

    with pytest.raises(MontoInvalido):
        RegistrarIngreso(repository).execute(
            datos,
            6
        )

    repository.create.assert_not_called()


def test_registrar_ingreso_con_fecha_invalida_lanza_fecha_invalida():

    repository = Mock()
    repository.existe_categoria.return_value = True
    repository.get_cuenta.return_value = None

    datos = datos_validos()
    datos["fecha"] = "fecha-invalida"

    with pytest.raises(FechaInvalida):
        RegistrarIngreso(repository).execute(
            datos,
            6
        )


def test_registrar_ingreso_con_categoria_inexistente_lanza_categoria_invalida():

    repository = Mock()
    repository.existe_categoria.return_value = False

    with pytest.raises(CategoriaInvalida):
        RegistrarIngreso(repository).execute(
            datos_validos(),
            6
        )

    repository.get_cuenta.assert_not_called()


def test_registrar_ingreso_con_cuenta_inexistente_lanza_cuenta_no_encontrada():

    repository = Mock()
    repository.existe_categoria.return_value = True
    repository.get_cuenta.return_value = None

    with pytest.raises(CuentaNoEncontrada):
        RegistrarIngreso(repository).execute(
            datos_validos(),
            6
        )

    repository.create.assert_not_called()


def test_registrar_ingreso_con_cuenta_de_otro_usuario_lanza_sin_permiso():

    repository = Mock()
    repository.existe_categoria.return_value = True

    cuenta = Mock()
    cuenta.id_usuario = 99
    repository.get_cuenta.return_value = cuenta

    with pytest.raises(CuentaNoPerteneceAlUsuario):
        RegistrarIngreso(repository).execute(
            datos_validos(),
            6
        )

    repository.create.assert_not_called()
    repository.aumentar_saldo.assert_not_called()


def test_registrar_ingreso_con_tipo_transaccion_invalido_lanza_error():

    repository = Mock()
    repository.existe_categoria.return_value = True

    cuenta = Mock()
    cuenta.id_usuario = 6
    cuenta.id_cuenta = 1
    cuenta.saldo = Decimal("100000.00")
    repository.get_cuenta.return_value = cuenta

    repository.get_tipo_transaccion.return_value = None

    with pytest.raises(TipoTransaccionNoValido):
        RegistrarIngreso(repository).execute(datos_validos(), 6)

    repository.create.assert_not_called()
    repository.aumentar_saldo.assert_not_called()


def test_registrar_ingreso_con_saldo_bajo_es_valido():

    repository = Mock()
    repository.existe_categoria.return_value = True

    cuenta = Mock()
    cuenta.id_usuario = 6
    cuenta.id_cuenta = 1
    cuenta.saldo = Decimal("0.00")
    repository.get_cuenta.return_value = cuenta

    tipo_ingreso = Mock()
    tipo_ingreso.id_tipo_transaccion = 1
    repository.get_tipo_transaccion.return_value = tipo_ingreso

    RegistrarIngreso(repository).execute(datos_validos(), 6)

    repository.create.assert_called_once()
    repository.aumentar_saldo.assert_called_once_with(
        1,
        Decimal("50000.00")
    )
