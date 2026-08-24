from typing import List

from fastapi import APIRouter, Depends

from app.core.security.auth import get_current_user

from app.modules.transaccion.application.use_cases.obtener_transacciones import (
    ObtenerTransaccionesUseCase
)
from app.modules.transaccion.application.use_cases.registrar_gasto import RegistrarGasto

from app.modules.transaccion.domain.interface.trans_repository import TransaccionRepository
from app.modules.transaccion.infrastructure.repository.sql_transaccion_repository import SqlTransaccionesRepository
from app.modules.transaccion.presentation.schema.trans_schema import (
    GastoRequest,
    GastoResponse,
    ListaTransaccionesResponse
)

from app.core.database.connection import get_db
from sqlalchemy.orm import Session




router = APIRouter(
    prefix="/transacciones",
    tags=["Transacciones"]
)


def get_transaccion_repository(
    db: Session = Depends(get_db)
) -> TransaccionRepository:
    return SqlTransaccionesRepository(db)


@router.post(
    "/gastos",
    response_model=GastoResponse,
    status_code=201
)
def registrar_gasto(
    gasto: GastoRequest,
    current_user: object = Depends(get_current_user),
    repository: TransaccionRepository = Depends(get_transaccion_repository),
):
    caso_uso = RegistrarGasto(repository)

    return caso_uso.execute(
        gasto.model_dump(),
        current_user.id_usuario
    )


@router.get(
    "/",
    response_model=List[ListaTransaccionesResponse],
    status_code=200
)
def obtener_transacciones(
    current_user: object = Depends(get_current_user),
    repository: TransaccionRepository = Depends(get_transaccion_repository),
):
    caso_uso = ObtenerTransaccionesUseCase(repository)

    return caso_uso.execute(current_user.id_usuario)
