from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database.connection import get_db
from app.core.security.auth import get_current_user

from app.modules.ahorro.domain.interface.ahorro_repository import AhorroRepository
from app.modules.ahorro.infrastructure.repository.sql_ahorro_repository import SqlAhorroRepository
from app.modules.ahorro.application.use_cases.crear_meta import CrearMeta
from app.modules.ahorro.application.use_cases.obtener_metas import ObtenerMetas
from app.modules.ahorro.application.use_cases.obtener_progreso_meta import ObtenerProgresoMeta
from app.modules.ahorro.application.use_cases.obtener_ahorro import ObtenerAhorrosUseCase
from app.modules.ahorro.application.use_cases.obtener_ahorro_por_id import ObtenerAhorroPorIdUseCase
from app.modules.ahorro.application.use_cases.actualizar_ahorro import ActualizarAhorroUseCase
from app.modules.ahorro.application.use_cases.eliminar_ahorro import EliminarAhorroUseCase

from app.modules.ahorro.presentation.schema.ahorro_schema import (
    AhorroCreate,
    AhorroResponse,
    MetaCreate,
    MetaResponse,
    AhorroProgresoResponse,
)


router = APIRouter(
    prefix="/ahorros",
    tags=["Ahorros"],
    dependencies=[Depends(get_current_user)]
)


def get_ahorro_repository(
    db: Session = Depends(get_db)
) -> AhorroRepository:
    return SqlAhorroRepository(db)


@router.post("/metas", response_model=MetaResponse, status_code=201)
def crear_meta(
    meta: MetaCreate,
    current_user: object = Depends(get_current_user),
    repository: AhorroRepository = Depends(get_ahorro_repository),
):
    caso_uso = CrearMeta(repository)
    return caso_uso.execute(meta.model_dump(), current_user.id_usuario)


@router.get("/metas", response_model=list[MetaResponse])
def obtener_metas(
    current_user: object = Depends(get_current_user),
    repository: AhorroRepository = Depends(get_ahorro_repository),
):
    caso_uso = ObtenerMetas(repository)
    return caso_uso.execute(current_user.id_usuario)


@router.get(
    "/{id_ahorro}/progreso",
    response_model=AhorroProgresoResponse,
    responses={
        200: {"description": "Progreso de la meta"},
        404: {"description": "Meta no encontrada"},
        500: {"description": "Error interno del servidor"},
    },
)
def obtener_progreso_meta(
    id_ahorro: int,
    current_user: object = Depends(get_current_user),
    repository: AhorroRepository = Depends(get_ahorro_repository),
):
    caso_uso = ObtenerProgresoMeta(repository)
    return caso_uso.execute(id_ahorro, current_user.id_usuario)


@router.get("/")
def obtener_ahorros(
    repository: AhorroRepository = Depends(get_ahorro_repository),
):
    caso_uso = ObtenerAhorrosUseCase(repository)
    return caso_uso.execute()


@router.get("/{id_ahorro}")
def obtener_ahorro_por_id(
    id_ahorro: int,
    repository: AhorroRepository = Depends(get_ahorro_repository),
):
    caso_uso = ObtenerAhorroPorIdUseCase(repository)
    return caso_uso.execute(id_ahorro)


@router.put("/{id_ahorro}")
def actualizar_ahorro(
    id_ahorro: int,
    ahorro: AhorroCreate,
    repository: AhorroRepository = Depends(get_ahorro_repository),
):
    caso_uso = ActualizarAhorroUseCase(repository)
    return caso_uso.execute(id_ahorro, ahorro.model_dump())


@router.delete("/{id_ahorro}")
def eliminar_ahorro(
    id_ahorro: int,
    repository: AhorroRepository = Depends(get_ahorro_repository),
):
    caso_uso = EliminarAhorroUseCase(repository)
    response = caso_uso.execute(id_ahorro)
    if not response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    return response
