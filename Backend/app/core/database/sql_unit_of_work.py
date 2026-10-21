from sqlalchemy.orm import Session

from app.core.database.unit_of_work import UnitOfWork
from app.modules.ahorro.infrastructure.repository.sql_ahorro_repository import (
    SqlAhorroRepository,
)
from app.modules.analytics.infrastructure.repository.sql_analytics_repository import (
    SqlAnalyticsRepository,
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


class SqlAlchemyUnitOfWork(UnitOfWork):

    def __init__(self, session: Session):
        self.session = session
        self.transacciones = SqlTransaccionesRepository(session)
        self.cuentas = SqlCuentaRepository(session)
        self.usuarios = SqlUsuarioRepository(session)
        self.auth = SqlAuthRepository(session, self.usuarios)
        self.ahorros = SqlAhorroRepository(session)
        self.analiticas = SqlAnalyticsRepository(session)
        self.programaciones = SqlProgramacionRepository(session)
        self.parentales = SqlControlParentalRepository(session)
        self.mesadas = SqlMesadaParentalRepository(session)
        self.ejecuciones = SqlEjecucionMesadaRepository(session)

    def commit(self) -> None:
        self.session.commit()

    def rollback(self) -> None:
        self.session.rollback()
