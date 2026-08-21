from datetime import date
from decimal import Decimal
from unittest.mock import Mock, patch

from app.modules.transaccion.domain.entity.trans_entity import Transaccion
from app.modules.transaccion.domain.interface.trans_repository import (
    TransaccionRepository
)
from app.modules.transaccion.infrastructure.repository.sql_transaccion_repository import (
    SqlTransaccionesRepository
)


def test_repositorio_implementa_la_interfaz_de_dominio():
    assert issubclass(SqlTransaccionesRepository, TransaccionRepository)


def test_find_by_usuario_retorna_entidades_de_dominio():

    db = Mock()

    registro = Mock()
    registro.id_transaccion = 1
    registro.monto = Decimal("50000.00")
    registro.id_tipo_transaccion = 1
    registro.fecha = date(2026, 1, 1)
    registro.descripcion = "Salario"
    registro.id_categoria = 3

    db.query.return_value.join.return_value.join.return_value.filter.return_value.order_by.return_value.all.return_value = [
        (registro, "INGRESO")
    ]

    resultado = SqlTransaccionesRepository(db).find_by_usuario(
        6
    )

    db.query.assert_called_once()
    db.query.return_value.join.assert_called_once()
    db.query.return_value.join.return_value.join.assert_called_once()
    db.query.return_value.join.return_value.join.return_value.filter.assert_called_once()
    db.query.return_value.join.return_value.join.return_value.filter.return_value.order_by.assert_called_once()
    db.query.return_value.join.return_value.join.return_value.filter.return_value.order_by.return_value.all.assert_called_once()

    assert len(resultado) == 1
    assert isinstance(resultado[0], Transaccion)
    assert resultado[0].id == 1
    assert resultado[0].monto == Decimal("50000.00")
    assert resultado[0].tipo == "INGRESO"
    assert resultado[0].fecha == date(2026, 1, 1)
    assert resultado[0].descripcion == "Salario"
    assert resultado[0].categoria == 3


def test_find_by_usuario_sin_registros_retorna_lista_vacia():

    db = Mock()
    db.query.return_value.join.return_value.join.return_value.filter.return_value.order_by.return_value.all.return_value = []

    resultado = SqlTransaccionesRepository(db).find_by_usuario(
        6
    )

    assert resultado == []


def test_get_tipo_transaccion_retorna_el_tipo_por_nombre():

    db = Mock()

    tipo = Mock()
    tipo.id_tipo_transaccion = 2
    tipo.nombre_tipo_transaccion = "GASTO"

    db.query.return_value.filter.return_value.first.return_value = tipo

    resultado = SqlTransaccionesRepository(db).get_tipo_transaccion(
        "GASTO"
    )

    assert resultado == tipo


def test_create_guarda_y_retorna_la_transaccion():

    db = Mock()

    transaccion_guardada = Mock()
    transaccion_guardada.id_transaccion = 1
    db.add.return_value = None
    db.refresh.return_value = None

    db.refresh.side_effect = lambda obj: obj.__dict__.update({
        "id_transaccion": transaccion_guardada.id_transaccion
    })

    datos = {
        "monto": Decimal("20000.00"),
        "fecha": date(2026, 1, 1),
        "descripcion": "Transporte",
        "id_cuenta": 1,
        "id_categoria": 3,
    }

    with patch(
        "app.modules.transaccion.infrastructure.repository."
        "sql_transaccion_repository.TransaccionModel"
    ) as modelo_mock:
        modelo_mock.return_value = transaccion_guardada

        resultado = SqlTransaccionesRepository(db).create(
            datos
        )

    modelo_mock.assert_called_once_with(**datos)
    db.add.assert_called_once_with(transaccion_guardada)
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(transaccion_guardada)

    assert resultado == transaccion_guardada


def test_descontar_saldo_resta_el_monto_de_la_cuenta():

    db = Mock()

    cuenta = Mock()
    cuenta.id_cuenta = 1
    cuenta.saldo = Decimal("100000.00")

    db.query.return_value.filter.return_value.first.return_value = cuenta

    resultado = SqlTransaccionesRepository(db).descontar_saldo(
        1,
        Decimal("20000.00")
    )

    assert cuenta.saldo == Decimal("80000.00")
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(cuenta)

    assert resultado == cuenta
