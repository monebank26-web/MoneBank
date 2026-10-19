from unittest.mock import Mock

from app.core.database.sql_unit_of_work import SqlAlchemyUnitOfWork
from app.modules.ahorro.infrastructure.repository.sql_ahorro_repository import (
    SqlAhorroRepository,
)
from app.modules.auth.infrastructure.repository.sql_auth_repository import (
    SqlAuthRepository,
)
from app.modules.control_parental.infrastructure.repository.sql_control_parental_repository import (
    SqlControlParentalRepository,
)
from app.modules.control_parental.infrastructure.repository.sql_ejecucion_mesada_repository import (
    SqlEjecucionMesadaRepository,
)
from app.modules.control_parental.infrastructure.repository.sql_mesada_parental_repository import (
    SqlMesadaParentalRepository,
)
from app.modules.cuenta.infrastructure.repository.sql_cuenta_repository import (
    SqlCuentaRepository,
)
from app.modules.programacion_ahorro.infrastructure.repository.sql_programacion_repository import (
    SqlProgramacionRepository,
)
from app.modules.transaccion.infrastructure.repository.sql_transaccion_repository import (
    SqlTransaccionesRepository,
)
from app.modules.usuario.infrastructure.repository.sql_usuario_repository import (
    SqlUsuarioRepository,
)


def test_instancia_repositorios_con_la_sesion():
    session = Mock()

    unit_of_work = SqlAlchemyUnitOfWork(session)

    assert isinstance(unit_of_work.transacciones, SqlTransaccionesRepository)
    assert isinstance(unit_of_work.cuentas, SqlCuentaRepository)
    assert unit_of_work.transacciones.db is session
    assert unit_of_work.cuentas.db is session


def test_instancia_repositorios_de_escritura_con_la_sesion():
    session = Mock()

    unit_of_work = SqlAlchemyUnitOfWork(session)

    assert isinstance(unit_of_work.usuarios, SqlUsuarioRepository)
    assert isinstance(unit_of_work.auth, SqlAuthRepository)
    assert isinstance(unit_of_work.ahorros, SqlAhorroRepository)
    assert isinstance(unit_of_work.programaciones, SqlProgramacionRepository)
    assert isinstance(unit_of_work.parentales, SqlControlParentalRepository)
    assert isinstance(unit_of_work.mesadas, SqlMesadaParentalRepository)
    assert isinstance(unit_of_work.ejecuciones, SqlEjecucionMesadaRepository)

    repositorios = (
        unit_of_work.usuarios,
        unit_of_work.ahorros,
        unit_of_work.programaciones,
        unit_of_work.parentales,
        unit_of_work.mesadas,
        unit_of_work.ejecuciones,
    )
    for repositorio in repositorios:
        assert repositorio.db is session

    assert unit_of_work.auth.db is session
    assert unit_of_work.auth.usuario_repository is unit_of_work.usuarios


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
