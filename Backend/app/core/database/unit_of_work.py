from abc import ABC, abstractmethod

from app.modules.cuenta.domain.interface.cuenta_repository import CuentaRepository
from app.modules.transaccion.domain.interface.trans_repository import (
    TransaccionRepository,
)


class UnitOfWork(ABC):

    transacciones: TransaccionRepository
    cuentas: CuentaRepository

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
