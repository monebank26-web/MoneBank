from sqlalchemy.orm import Session

from app.core.database.unit_of_work import UnitOfWork
from app.modules.admin.infrastructure.repository.sql_registro_accion_admin_repository import (
    SqlRegistroAccionAdminRepository,
)
from app.modules.cuenta.infrastructure.repository.sql_cuenta_repository import (
    SqlCuentaRepository,
)
from app.modules.transaccion.infrastructure.repository.sql_transaccion_repository import (
    SqlTransaccionesRepository,
)


class SqlAlchemyUnitOfWork(UnitOfWork):

    def __init__(self, session: Session):
        self.session = session
        self.transacciones = SqlTransaccionesRepository(session)
        self.cuentas = SqlCuentaRepository(session)
        self.registros_accion_admin = SqlRegistroAccionAdminRepository(session)

    def commit(self) -> None:
        self.session.commit()

    def rollback(self) -> None:
        self.session.rollback()
