from datetime import date
from typing import List, Optional

from fastapi import APIRouter, Depends, Query, HTTPException

from app.core.security.auth import get_current_user

from app.modules.transaccion.application.use_cases.obtener_transacciones_historial import ObtenerHistorialUseCase
from app.modules.transaccion.application.use_cases.registrar_gasto import RegistrarGasto

from app.modules.transaccion.domain.interface.trans_repository import TransaccionRepository
from app.modules.transaccion.infrastructure.repository.sql_transaccion_repository import SqlTransaccionesRepository
from app.modules.transaccion.presentation.schema.trans_schema import (
    CategoriaResponse,
    GastoRequest,
    GastoResponse,
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
    pagina: int = Query(1, ge=1),
    por_pagina: int = Query(10, ge=1, le=100),
    ordenar_por: str = Query("fecha", pattern="^(fecha|monto)$"),
    orden: str = Query("desc", pattern="^(asc|desc)$"),
    fecha_inicio: Optional[date] = None,
    fecha_fin: Optional[date] = None,
    monto_min: Optional[float] = None,
    monto_max: Optional[float] = None,
    busqueda: Optional[str] = Query(None, max_length=100),
    id_tipo_transaccion: Optional[int] = Query(None, gt=0),
    id_categoria: Optional[int] = Query(None, gt=0),
):
    if fecha_inicio and fecha_fin and fecha_inicio > fecha_fin:
        raise HTTPException(422, "fecha_inicio no puede ser mayor a fecha_fin")
    if monto_min is not None and monto_max is not None and monto_min > monto_max:
        raise HTTPException(422, "monto_min no puede ser mayor a monto_max")

    filtros = {
        "pagina": pagina, "por_pagina": por_pagina,
        "ordenar_por": ordenar_por, "orden": orden,
        "fecha_inicio": fecha_inicio, "fecha_fin": fecha_fin,
        "monto_min": monto_min, "monto_max": monto_max,
        "busqueda": busqueda,
        "id_tipo_transaccion": id_tipo_transaccion,
        "id_categoria": id_categoria,
    }
    caso_uso = ObtenerHistorialUseCase(repository)
    return caso_uso.execute(current_user.id_usuario, filtros)


@router.get("/categorias", response_model=List[CategoriaResponse], status_code=200)
def obtener_categorias(
    current_user: object = Depends(get_current_user),
    repository: TransaccionRepository = Depends(get_transaccion_repository),
):
    return repository.find_categorias()