from unittest.mock import Mock

import pytest

from app.core.database.sql_unit_of_work import SqlAlchemyUnitOfWork
from app.core.database.uow_factory import abrir_unit_of_work, crear_unit_of_work


def test_crear_unit_of_work_usa_la_sesion_recibida():
    session = Mock()

    unit_of_work = crear_unit_of_work(session)

    assert isinstance(unit_of_work, SqlAlchemyUnitOfWork)
    assert unit_of_work.transacciones.db is session
    assert unit_of_work.cuentas.db is session


def test_abrir_unit_of_work_cierra_la_sesion_al_salir():
    session = Mock()

    with abrir_unit_of_work(lambda: session) as unit_of_work:
        assert isinstance(unit_of_work, SqlAlchemyUnitOfWork)

    session.close.assert_called_once()


def test_abrir_unit_of_work_no_hace_commit_automatico():
    session = Mock()

    with abrir_unit_of_work(lambda: session):
        pass

    session.commit.assert_not_called()


def test_abrir_unit_of_work_hace_rollback_y_cierra_ante_excepcion():
    session = Mock()

    with pytest.raises(RuntimeError):
        with abrir_unit_of_work(lambda: session):
            raise RuntimeError("fallo")

    session.rollback.assert_called_once()
    session.close.assert_called_once()


def test_abrir_unit_of_work_cierra_si_falla_la_creacion(monkeypatch):
    session = Mock()

    def fallar_al_crear(_session):
        raise RuntimeError("fallo al crear")

    monkeypatch.setattr(
        "app.core.database.uow_factory.crear_unit_of_work",
        fallar_al_crear,
    )

    with pytest.raises(RuntimeError):
        with abrir_unit_of_work(lambda: session):
            pass

    session.close.assert_called_once()
