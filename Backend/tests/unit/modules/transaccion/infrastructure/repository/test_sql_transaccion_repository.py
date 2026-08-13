from datetime import date
from decimal import Decimal
from unittest.mock import Mock

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
    registro.tipo = "INGRESO"
    registro.fecha = date(2026, 1, 1)
    registro.descripcion = "Salario"
    registro.id_categoria = 3

    db.query.return_value.join.return_value.filter.return_value.all.return_value = [
        registro
    ]

    resultado = SqlTransaccionesRepository(db).find_by_usuario(
        6
    )

    db.query.assert_called_once()
    db.query.return_value.join.assert_called_once()
    db.query.return_value.join.return_value.filter.assert_called_once()
    db.query.return_value.join.return_value.filter.return_value.all.assert_called_once()

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
    db.query.return_value.join.return_value.filter.return_value.all.return_value = []

    resultado = SqlTransaccionesRepository(db).find_by_usuario(
        6
    )

    assert resultado == []
