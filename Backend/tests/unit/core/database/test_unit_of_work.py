from unittest.mock import Mock

from app.core.database.sql_unit_of_work import SqlAlchemyUnitOfWork
from app.modules.cuenta.infrastructure.repository.sql_cuenta_repository import (
    SqlCuentaRepository,
)
from app.modules.transaccion.infrastructure.repository.sql_transaccion_repository import (
    SqlTransaccionesRepository,
)


def test_instancia_repositorios_con_la_sesion():
    session = Mock()

    unit_of_work = SqlAlchemyUnitOfWork(session)

    assert isinstance(unit_of_work.transacciones, SqlTransaccionesRepository)
    assert isinstance(unit_of_work.cuentas, SqlCuentaRepository)
    assert unit_of_work.transacciones.db is session
    assert unit_of_work.cuentas.db is session


def test_commit_delega_en_la_sesion():
    session = Mock()
    unit_of_work = SqlAlchemyUnitOfWork(session)

    unit_of_work.commit()

    session.commit.assert_called_once()


def test_rollback_delega_en_la_sesion():
    session = Mock()
    unit_of_work = SqlAlchemyUnitOfWork(session)

    unit_of_work.rollback()

    session.rollback.assert_called_once()


def test_context_manager_hace_rollback_ante_excepcion():
    session = Mock()
    unit_of_work = SqlAlchemyUnitOfWork(session)

    try:
        with unit_of_work:
            raise RuntimeError("fallo")
    except RuntimeError:
        pass

    session.rollback.assert_called_once()
    session.commit.assert_not_called()


def test_context_manager_no_hace_rollback_si_todo_va_bien():
    session = Mock()
    unit_of_work = SqlAlchemyUnitOfWork(session)

    with unit_of_work:
        unit_of_work.commit()

    session.commit.assert_called_once()
    session.rollback.assert_not_called()
