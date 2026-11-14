from datetime import date

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.database.base import Base
from app.modules.programacion_ahorro.infrastructure.model.programacion_model import (
    ProgramacionModel,
)
from app.modules.programacion_ahorro.infrastructure.repository.sql_programacion_repository import (
    SqlProgramacionRepository,
)


@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine, tables=[ProgramacionModel.__table__])
    Session = sessionmaker(bind=engine)
    sesion = Session()
    try:
        yield sesion
    finally:
        sesion.close()


def crear_programacion(session, **cambios):
    datos = {
        "id_ahorro": 5,
        "monto_periodico": 50000,
        "fecha_cobro": date(2026, 11, 1),
        "frecuencia": "MENSUAL",
        "fecha_inicio": date(2026, 11, 1),
        "fecha_fin": None,
        "estado": "ACTIVA",
    }
    datos.update(cambios)

    programacion = ProgramacionModel(**datos)
    session.add(programacion)
    session.commit()
    return programacion


def test_update_estado_persiste_el_cambio(session):

    programacion = crear_programacion(session)
    repository = SqlProgramacionRepository(session)

    resultado = repository.update_estado(
        programacion.id_programacion_ahorro,
        "PAUSADA",
    )

    assert resultado.estado == "PAUSADA"

    session.expire_all()
    guardada = session.get(ProgramacionModel, programacion.id_programacion_ahorro)
    assert guardada.estado == "PAUSADA"


def test_update_estado_devuelve_none_si_no_existe(session):

    repository = SqlProgramacionRepository(session)

    assert repository.update_estado(999, "PAUSADA") is None


def test_update_periodicidad_persiste_monto_y_frecuencia(session):

    programacion = crear_programacion(session)
    repository = SqlProgramacionRepository(session)

    resultado = repository.update_periodicidad(
        programacion.id_programacion_ahorro,
        75000,
        "SEMANAL",
    )

    assert resultado.monto_periodico == 75000
    assert resultado.frecuencia == "SEMANAL"

    session.expire_all()
    guardada = session.get(ProgramacionModel, programacion.id_programacion_ahorro)
    assert guardada.monto_periodico == 75000
    assert guardada.frecuencia == "SEMANAL"


def test_update_periodicidad_devuelve_none_si_no_existe(session):

    repository = SqlProgramacionRepository(session)

    assert repository.update_periodicidad(999, 75000, "SEMANAL") is None


def test_get_by_id_devuelve_la_programacion(session):

    programacion = crear_programacion(session)
    repository = SqlProgramacionRepository(session)

    encontrada = repository.get_by_id(programacion.id_programacion_ahorro)

    assert encontrada.id_ahorro == 5
