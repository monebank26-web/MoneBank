from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database.connection import get_db
from app.core.security.auth import get_current_user

from app.modules.transaccion.application.use_cases.obtener_transacciones import (
    ObtenerTransaccionesUseCase
)
from app.modules.transaccion.domain.interface.trans_repository import (
    TransaccionRepository
)
from app.modules.transaccion.infrastructure.repository.sql_transaccion_repository import (
    SqlTransaccionesRepository
)
from app.modules.transaccion.presentation.schema.trans_schema import (
    ListaTransaccionesResponse
)
from app.shared.exceptions.transaccion import TransaccionesNoEncontrado


router = APIRouter(
    prefix="/transacciones",
    tags=["transacciones"]
)


def get_transaccion_repository(
    db: Session = Depends(get_db)
) -> TransaccionRepository:
    return SqlTransaccionesRepository(db)


@router.get(
    "/",
    response_model=List[ListaTransaccionesResponse],
    status_code=200
)
def obtener_transacciones(
    current_user: object = Depends(get_current_user),
    repository: TransaccionRepository = Depends(get_transaccion_repository)
):
    caso_uso = ObtenerTransaccionesUseCase(repository)

    try:
        return caso_uso.execute(current_user.id_usuario)
    except TransaccionesNoEncontrado:
        raise HTTPException(
            status_code=404,
            detail="No se encontraron transacciones"
        )
