from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database.connection import get_db
from app.core.security.auth import get_current_user

from app.modules.ahorro.domain.interface.ahorro_repository import AhorroRepository
from app.modules.ahorro.infrastructure.repository.sql_ahorro_repository import SqlAhorroRepository
from app.modules.ahorro.application.use_cases.crear_meta import CrearMeta
from app.modules.ahorro.application.use_cases.obtener_metas import ObtenerMetas
from app.modules.ahorro.application.use_cases.crear_limite import CrearLimite
from app.modules.ahorro.application.use_cases.obtener_limites import ObtenerLimites
from app.modules.ahorro.application.use_cases.obtener_alertas_presupuesto import ObtenerAlertasPresupuesto
from app.modules.ahorro.application.use_cases.obtener_progreso_meta import ObtenerProgresoMeta
from app.modules.ahorro.application.use_cases.obtener_ahorro import ObtenerAhorrosUseCase
from app.modules.ahorro.application.use_cases.obtener_ahorro_por_id import ObtenerAhorroPorIdUseCase
from app.modules.ahorro.application.use_cases.actualizar_ahorro import ActualizarAhorroUseCase
from app.modules.ahorro.application.use_cases.eliminar_ahorro import EliminarAhorroUseCase

from app.modules.cuenta.domain.interface.cuenta_repository import CuentaRepository
from app.modules.cuenta.infrastructure.repository.sql_cuenta_repository import SqlCuentaRepository

from app.modules.ahorro.presentation.schema.ahorro_schema import (
    AhorroCreate,
    AhorroResponse,
    MetaCreate,
    MetaResponse,
    AhorroProgresoResponse,
    LimiteCreate,
    LimiteResponse,
    AlertaResponse,
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


def get_cuenta_repository(
    db: Session = Depends(get_db)
) -> CuentaRepository:
    return SqlCuentaRepository(db)


@router.post("/metas", response_model=MetaResponse, status_code=201)
def crear_meta(
    meta: MetaCreate,
    current_user: object = Depends(get_current_user),
    repository: AhorroRepository = Depends(get_ahorro_repository),
    cuenta_repository: CuentaRepository = Depends(get_cuenta_repository),
):
    caso_uso = CrearMeta(repository, cuenta_repository)
    return caso_uso.execute(meta.model_dump(), current_user.id_usuario)


@router.get("/metas", response_model=list[MetaResponse])
def obtener_metas(
    current_user: object = Depends(get_current_user),
    repository: AhorroRepository = Depends(get_ahorro_repository),
    cuenta_repository: CuentaRepository = Depends(get_cuenta_repository),
):
    caso_uso = ObtenerMetas(repository, cuenta_repository)
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
    cuenta_repository: CuentaRepository = Depends(get_cuenta_repository),
):
    caso_uso = ObtenerProgresoMeta(repository, cuenta_repository)
    return caso_uso.execute(id_ahorro, current_user.id_usuario)


@router.post("/limites", response_model=LimiteResponse, status_code=201)
def crear_limite(
    limite: LimiteCreate,
    current_user: object = Depends(get_current_user),
    repository: AhorroRepository = Depends(get_ahorro_repository),
    cuenta_repository: CuentaRepository = Depends(get_cuenta_repository),
):
    caso_uso = CrearLimite(repository, cuenta_repository)
    return caso_uso.execute(limite.model_dump(), current_user.id_usuario)


@router.get("/limites", response_model=list[LimiteResponse])
def obtener_limites(
    current_user: object = Depends(get_current_user),
    repository: AhorroRepository = Depends(get_ahorro_repository),
    cuenta_repository: CuentaRepository = Depends(get_cuenta_repository),
):
    caso_uso = ObtenerLimites(repository, cuenta_repository)
    return caso_uso.execute(current_user.id_usuario)


@router.get("/limites/alertas", response_model=list[AlertaResponse])
def obtener_alertas_presupuesto(
    current_user: object = Depends(get_current_user),
    repository: AhorroRepository = Depends(get_ahorro_repository),
    cuenta_repository: CuentaRepository = Depends(get_cuenta_repository),
):
    caso_uso = ObtenerAlertasPresupuesto(repository, cuenta_repository)
    return caso_uso.execute(current_user.id_usuario)


@router.get("/", response_model=list[AhorroResponse])
def obtener_ahorros(
    current_user: object = Depends(get_current_user),
    repository: AhorroRepository = Depends(get_ahorro_repository),
    cuenta_repository: CuentaRepository = Depends(get_cuenta_repository),
):
    caso_uso = ObtenerAhorrosUseCase(repository, cuenta_repository)
    return caso_uso.execute(current_user.id_usuario)


@router.get("/{id_ahorro}", response_model=AhorroResponse)
def obtener_ahorro_por_id(
    id_ahorro: int,
    current_user: object = Depends(get_current_user),
    repository: AhorroRepository = Depends(get_ahorro_repository),
    cuenta_repository: CuentaRepository = Depends(get_cuenta_repository),
):
    caso_uso = ObtenerAhorroPorIdUseCase(repository, cuenta_repository)
    return caso_uso.execute(id_ahorro, current_user.id_usuario)


@router.put("/{id_ahorro}", response_model=AhorroResponse)
def actualizar_ahorro(
    id_ahorro: int,
    ahorro: AhorroCreate,
    current_user: object = Depends(get_current_user),
    repository: AhorroRepository = Depends(get_ahorro_repository),
    cuenta_repository: CuentaRepository = Depends(get_cuenta_repository),
):
    caso_uso = ActualizarAhorroUseCase(repository, cuenta_repository)
    return caso_uso.execute(id_ahorro, ahorro.model_dump(), current_user.id_usuario)


@router.delete("/{id_ahorro}")
def eliminar_ahorro(
    id_ahorro: int,
    current_user: object = Depends(get_current_user),
    repository: AhorroRepository = Depends(get_ahorro_repository),
    cuenta_repository: CuentaRepository = Depends(get_cuenta_repository),
):
    caso_uso = EliminarAhorroUseCase(repository, cuenta_repository)
    return caso_uso.execute(id_ahorro, current_user.id_usuario)