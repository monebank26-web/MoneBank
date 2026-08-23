from typing import List

from fastapi import APIRouter, Depends

from app.core.security.auth import get_current_user

from app.modules.transaccion.application.use_cases.obtener_detalle_transaccion import ObtenerDetalleUseCase
from app.modules.transaccion.application.use_cases.obtener_transacciones_historial import ObtenerHistorialUseCase
from app.modules.transaccion.application.use_cases.registrar_gasto import RegistrarGasto

from app.modules.transaccion.domain.interface.trans_repository import TransaccionRepository
from app.modules.transaccion.infrastructure.repository.sql_transaccion_repository import SqlTransaccionesRepository
from app.modules.transaccion.presentation.schema.trans_schema import (
    CategoriaResponse,
    DetalleTransaccionResponse,
    GastoRequest,
    GastoResponse,
    HistorialRequest,
    HistorialPaginadoResponse
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


@router.get("/historial", response_model=HistorialPaginadoResponse, status_code=200)
def obtener_historial(
    current_user: object = Depends(get_current_user),
    repository: TransaccionRepository = Depends(get_transaccion_repository),
    filtros: HistorialRequest = Depends(),
):
    caso_uso = ObtenerHistorialUseCase(repository)
    return caso_uso.execute(current_user.id_usuario, filtros.model_dump())


@router.get("/categorias", response_model=List[CategoriaResponse], status_code=200)
def obtener_categorias(
    current_user: object = Depends(get_current_user),
    repository: TransaccionRepository = Depends(get_transaccion_repository),
):
    return repository.find_categorias()


@router.get("/{id_transaccion}", response_model=DetalleTransaccionResponse, status_code=200)
def obtener_detalle(
    id_transaccion: int,
    current_user: object = Depends(get_current_user),
    repository: TransaccionRepository = Depends(get_transaccion_repository)
    
):
    caso_uso = ObtenerDetalleUseCase(repository)
    return caso_uso.execute(current_user.id_usuario, id_transaccion)