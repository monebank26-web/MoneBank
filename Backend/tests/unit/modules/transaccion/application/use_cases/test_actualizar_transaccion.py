from decimal import Decimal
from unittest.mock import Mock

import pytest

from app.modules.transaccion.application.use_cases.actualizar_transaccion import (
    ActualizarTransaccion
)
from app.shared.exceptions.business_exceptions import (
    CategoriaInvalida,
    CuentaNoEncontrada,
    CuentaNoPerteneceAlUsuario,
    MontoInvalido,
    SaldoInsuficiente,
    TransaccionNoEditable,
    TransaccionesNoEncontrado,
)

ID_GASTO = 2
ID_INGRESO = 1
ID_MOV_AHORRO = 3


def datos_update(monto="30000.00", id_categoria=3, descripcion="Actualizado"):
    return {
        "monto": Decimal(monto),
        "descripcion": descripcion,
        "id_categoria": id_categoria,
    }


def tipos(repository, id_gasto=ID_GASTO, id_ingreso=ID_INGRESO):
    tipo_gasto = Mock()
    tipo_gasto.id_tipo_transaccion = id_gasto
    tipo_ingreso = Mock()
    tipo_ingreso.id_tipo_transaccion = id_ingreso
    repository.get_tipo_transaccion.side_effect = lambda nombre: (
        tipo_gasto if nombre == "GASTO" else tipo_ingreso
    )


def test_actualizar_gasto_recalcula_saldo_exitosamente():

    repository = Mock()
    tipos(repository)
    repository.existe_categoria.return_value = True

    transaccion = Mock()
    transaccion.id_transaccion = 10
    transaccion.id_cuenta = 1
    transaccion.id_tipo_transaccion = ID_GASTO
    transaccion.monto = Decimal("50000.00")
    transaccion.estado = "COMPLETADA"
    repository.get_transaccion.return_value = transaccion

    cuenta = Mock()
    cuenta.id_usuario = 6
    cuenta.id_cuenta = 1
    cuenta.saldo = Decimal("100000.00")
    repository.get_cuenta.return_value = cuenta

    datos = datos_update(monto="30000.00")
    ActualizarTransaccion(repository).execute(10, datos, 6)

    args = repository.update_transaccion.call_args.args
    assert args[0] is transaccion
    assert args[1] == datos
    assert args[2] == 1
    assert args[3] == Decimal("120000.00")


def test_actualizar_ingreso_recalcula_saldo_exitosamente():

    repository = Mock()
    tipos(repository)
    repository.existe_categoria.return_value = True

    transaccion = Mock()
    transaccion.id_cuenta = 1
    transaccion.id_tipo_transaccion = ID_INGRESO
    transaccion.monto = Decimal("50000.00")
    transaccion.estado = "COMPLETADA"
    repository.get_transaccion.return_value = transaccion

    cuenta = Mock()
    cuenta.id_usuario = 6
    cuenta.id_cuenta = 1
    cuenta.saldo = Decimal("100000.00")
    repository.get_cuenta.return_value = cuenta

    ActualizarTransaccion(repository).execute(10, datos_update(monto="80000.00"), 6)

    assert repository.update_transaccion.call_args.args[3] == Decimal("130000.00")


def test_actualizar_gasto_que_supera_saldo_lanza_error():

    repository = Mock()
    tipos(repository)
    repository.existe_categoria.return_value = True

    transaccion = Mock()
    transaccion.id_cuenta = 1
    transaccion.id_tipo_transaccion = ID_GASTO
    transaccion.monto = Decimal("50000.00")
    transaccion.estado = "COMPLETADA"
    repository.get_transaccion.return_value = transaccion

    cuenta = Mock()
    cuenta.id_usuario = 6
    cuenta.id_cuenta = 1
    cuenta.saldo = Decimal("10000.00")
    repository.get_cuenta.return_value = cuenta

    with pytest.raises(SaldoInsuficiente):
        ActualizarTransaccion(repository).execute(10, datos_update(monto="70000.00"), 6)

    repository.update_transaccion.assert_not_called()


def test_actualizar_transaccion_inexistente_lanza_error():

    repository = Mock()
    repository.get_transaccion.return_value = None

    with pytest.raises(TransaccionesNoEncontrado):
        ActualizarTransaccion(repository).execute(999, datos_update(), 6)

    repository.update_transaccion.assert_not_called()


def test_actualizar_cuenta_de_otro_usuario_lanza_error():

    repository = Mock()
    tipos(repository)

    transaccion = Mock()
    transaccion.id_cuenta = 1
    repository.get_transaccion.return_value = transaccion

    cuenta = Mock()
    cuenta.id_usuario = 99
    repository.get_cuenta.return_value = cuenta

    with pytest.raises(CuentaNoPerteneceAlUsuario):
        ActualizarTransaccion(repository).execute(10, datos_update(), 6)


def test_actualizar_cuenta_inexistente_lanza_error():

    repository = Mock()
    transaccion = Mock()
    transaccion.id_cuenta = 1
    repository.get_transaccion.return_value = transaccion
    repository.get_cuenta.return_value = None

    with pytest.raises(CuentaNoEncontrada):
        ActualizarTransaccion(repository).execute(10, datos_update(), 6)


def test_actualizar_movimiento_ahorro_no_es_editable():

    repository = Mock()
    tipos(repository)

    transaccion = Mock()
    transaccion.id_cuenta = 1
    transaccion.id_tipo_transaccion = ID_MOV_AHORRO
    repository.get_transaccion.return_value = transaccion

    cuenta = Mock()
    cuenta.id_usuario = 6
    repository.get_cuenta.return_value = cuenta

    with pytest.raises(TransaccionNoEditable):
        ActualizarTransaccion(repository).execute(10, datos_update(), 6)


def test_actualizar_transaccion_cancelada_no_es_editable():

    repository = Mock()
    tipos(repository)

    transaccion = Mock()
    transaccion.id_cuenta = 1
    transaccion.id_tipo_transaccion = ID_GASTO
    transaccion.estado = "CANCELADA"
    repository.get_transaccion.return_value = transaccion

    cuenta = Mock()
    cuenta.id_usuario = 6
    repository.get_cuenta.return_value = cuenta

    with pytest.raises(TransaccionNoEditable):
        ActualizarTransaccion(repository).execute(10, datos_update(), 6)


def test_actualizar_con_monto_invalido_lanza_error():

    repository = Mock()
    tipos(repository)

    transaccion = Mock()
    transaccion.id_cuenta = 1
    transaccion.id_tipo_transaccion = ID_GASTO
    transaccion.estado = "COMPLETADA"
    repository.get_transaccion.return_value = transaccion

    cuenta = Mock()
    cuenta.id_usuario = 6
    repository.get_cuenta.return_value = cuenta

    with pytest.raises(MontoInvalido):
        ActualizarTransaccion(repository).execute(10, datos_update(monto="0.00"), 6)


def test_actualizar_con_categoria_inexistente_lanza_error():

    repository = Mock()
    tipos(repository)
    repository.existe_categoria.return_value = False

    transaccion = Mock()
    transaccion.id_cuenta = 1
    transaccion.id_tipo_transaccion = ID_GASTO
    transaccion.estado = "COMPLETADA"
    repository.get_transaccion.return_value = transaccion

    cuenta = Mock()
    cuenta.id_usuario = 6
    repository.get_cuenta.return_value = cuenta

    with pytest.raises(CategoriaInvalida):
        ActualizarTransaccion(repository).execute(10, datos_update(), 6)
