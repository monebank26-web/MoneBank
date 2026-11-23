from datetime import date
from unittest.mock import Mock

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


def test_obtener_vencidas_devuelve_solo_activas_y_vencidas(session):
    vencida = crear_programacion(session, fecha_cobro=date(2026, 3, 1))
    crear_programacion(session, fecha_cobro=date(2026, 4, 1))
    crear_programacion(
        session,
        fecha_cobro=date(2026, 2, 1),
        estado="PAUSADA",
    )

    repository = SqlProgramacionRepository(session)

    resultado = repository.obtener_vencidas(date(2026, 3, 19))

    assert [
        programacion.id_programacion_ahorro for programacion in resultado
    ] == [vencida.id_programacion_ahorro]


def test_get_para_procesar_bloquea_la_fila():
    db = Mock()
    consulta = Mock()
    db.query.return_value = consulta
    consulta.filter.return_value = consulta
    consulta.with_for_update.return_value = consulta
    consulta.first.return_value = object()

    repository = SqlProgramacionRepository(db)

    resultado = repository.get_para_procesar(7)

    consulta.with_for_update.assert_called_once_with(skip_locked=True)
    assert resultado is consulta.first.return_value


def test_actualizar_fecha_cobro_persiste_fecha_y_estado(session):
    programacion = crear_programacion(session)
    repository = SqlProgramacionRepository(session)
    nueva_fecha = date(2026, 12, 1)

    resultado = repository.actualizar_fecha_cobro(
        programacion.id_programacion_ahorro,
        nueva_fecha,
        "FINALIZADA",
    )

    assert resultado.fecha_cobro == nueva_fecha
    assert resultado.estado == "FINALIZADA"

    session.expire_all()
    guardada = session.get(ProgramacionModel, programacion.id_programacion_ahorro)
    assert guardada.fecha_cobro == nueva_fecha
    assert guardada.estado == "FINALIZADA"


def test_actualizar_fecha_cobro_devuelve_none_si_no_existe(session):
    repository = SqlProgramacionRepository(session)

    assert repository.actualizar_fecha_cobro(999, date(2026, 12, 1)) is None
