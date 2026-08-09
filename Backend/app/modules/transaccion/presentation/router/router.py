from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database.connection import get_db

from app.modules.transaccion.infrastucture.repository.sql_transaccion_repository import (
    SqlTransaccionRepository
)

from app.modules.transaccion.application.use_cases.registrar_gasto import (
    RegistrarGasto
)

from app.modules.transaccion.presentation.schema.transSchema import (
    GastoRequest,
    GastoResponse
)

router = APIRouter(
    prefix="/transacciones",
    tags=["Transacciones"]
)


@router.post("/gastos", response_model=GastoResponse)
def registrar_gasto(
    gasto: GastoRequest,
    db: Session = Depends(get_db)
):

    caso_uso = RegistrarGasto(
        SqlTransaccionRepository()
    )

    return caso_uso.execute(
        db,
        gasto.model_dump()
    )