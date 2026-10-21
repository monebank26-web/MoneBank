from abc import ABC, abstractmethod

from app.modules.ahorro.domain.interface.ahorro_repository import AhorroRepository
from app.modules.analytics.domain.interface.analytics_repository import (
    AnalyticsRepository,
)
from app.modules.auth.domain.interface.auth_repository import AuthRepository
from app.modules.control_parental.domain.interface.control_parental_repository import (
    ControlParentalRepository,
)
from app.modules.control_parental.domain.interface.ejecucion_mesada_repository import (
    EjecucionMesadaRepository,
)
from app.modules.control_parental.domain.interface.mesada_parental_repository import (
    MesadaParentalRepository,
)
from app.modules.cuenta.domain.interface.cuenta_repository import CuentaRepository
from app.modules.programacion_ahorro.domain.interface.programacion_repository import (
    ProgramacionAhorroRepository,
)
from app.modules.transaccion.domain.interface.trans_repository import (
    TransaccionRepository,
)
from app.modules.usuario.domain.interface.usuario_repository import UsuarioRepository


class UnitOfWork(ABC):

    transacciones: TransaccionRepository
    cuentas: CuentaRepository
    usuarios: UsuarioRepository
    auth: AuthRepository
    ahorros: AhorroRepository
    analiticas: AnalyticsRepository
    programaciones: ProgramacionAhorroRepository
    parentales: ControlParentalRepository
    mesadas: MesadaParentalRepository
    ejecuciones: EjecucionMesadaRepository

    def __enter__(self) -> "UnitOfWork":
        return self

    def __exit__(self, exc_type, exc, traceback) -> None:
        if exc_type is not None:
            self.rollback()

    @abstractmethod
    def commit(self) -> None:
        pass

    @abstractmethod
    def rollback(self) -> None:
        pass
