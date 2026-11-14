from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database.connection import get_db
from app.core.database.sql_unit_of_work import SqlAlchemyUnitOfWork
from app.core.database.unit_of_work import UnitOfWork
from app.modules.cuenta.domain.interface.cuenta_repository import CuentaRepository
from app.modules.cuenta.infrastructure.repository.sql_cuenta_repository import (
    SqlCuentaRepository,
)
from app.modules.transaccion.domain.interface.trans_repository import (
    TransaccionRepository,
)
from app.modules.transaccion.infrastructure.repository.sql_transaccion_repository import (
    SqlTransaccionesRepository,
)


def get_unit_of_work(db: Session = Depends(get_db)) -> UnitOfWork:
    return SqlAlchemyUnitOfWork(db)


def get_transaccion_repository(
    db: Session = Depends(get_db)
) -> TransaccionRepository:
    return SqlTransaccionesRepository(db)


def get_cuenta_repository(
    db: Session = Depends(get_db)
) -> CuentaRepository:
    return SqlCuentaRepository(db)
