from fastapi import APIRouter, Depends

from app.core.security.auth import get_current_user

from app.modules.ahorro.presentation.controller.ahorro_controller import (
    AhorroController,
    get_ahorro_controller,
)
from app.modules.ahorro.presentation.schema.ahorro_schema import (
    AhorroCreate,
    AhorroResponse,
    AlertaResponse,
    AhorroProgresoResponse,
    LimiteCreate,
    LimiteResponse,
    MetaCreate,
    MetaResponse,
    ResumenGlobalMetasResponse,
)


router = APIRouter(
    prefix="/ahorros",
    tags=["Ahorros"],
    dependencies=[Depends(get_current_user)]
)


@router.post("/metas", response_model=MetaResponse, status_code=201)
def crear_meta(
    meta: MetaCreate,
    current_user: object = Depends(get_current_user),
    controller: AhorroController = Depends(get_ahorro_controller),
):
    return controller.crear_meta(meta, current_user)


@router.get("/metas", response_model=list[MetaResponse])
def obtener_metas(
    current_user: object = Depends(get_current_user),
    controller: AhorroController = Depends(get_ahorro_controller),
):
    return controller.obtener_metas(current_user)


@router.get(
    "/metas/resumen",
    response_model=ResumenGlobalMetasResponse,
    responses={
        200: {"description": "Resumen global consolidado de todas las metas"},
        404: {"description": "Cuenta no encontrada"},
        500: {"description": "Error interno del servidor"},
    },
)
def obtener_resumen_global_metas(
    current_user: object = Depends(get_current_user),
    controller: AhorroController = Depends(get_ahorro_controller),
):
    return controller.obtener_resumen_global_metas(current_user)


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
    controller: AhorroController = Depends(get_ahorro_controller),
):
    return controller.obtener_progreso_meta(id_ahorro, current_user)


@router.post("/limites", response_model=LimiteResponse, status_code=201)
def crear_limite(
    limite: LimiteCreate,
    current_user: object = Depends(get_current_user),
    controller: AhorroController = Depends(get_ahorro_controller),
):
    return controller.crear_limite(limite, current_user)


@router.get("/limites", response_model=list[LimiteResponse])
def obtener_limites(
    current_user: object = Depends(get_current_user),
    controller: AhorroController = Depends(get_ahorro_controller),
):
    return controller.obtener_limites(current_user)


@router.get("/limites/alertas", response_model=list[AlertaResponse])
def obtener_alertas_presupuesto(
    current_user: object = Depends(get_current_user),
    controller: AhorroController = Depends(get_ahorro_controller),
):
    return controller.obtener_alertas_presupuesto(current_user)


@router.get("/", response_model=list[AhorroResponse])
def obtener_ahorros(
    current_user: object = Depends(get_current_user),
    controller: AhorroController = Depends(get_ahorro_controller),
):
    return controller.obtener_ahorros(current_user)


@router.get("/{id_ahorro}", response_model=AhorroResponse)
def obtener_ahorro_por_id(
    id_ahorro: int,
    current_user: object = Depends(get_current_user),
    controller: AhorroController = Depends(get_ahorro_controller),
):
    return controller.obtener_ahorro_por_id(id_ahorro, current_user)


@router.put("/{id_ahorro}", response_model=AhorroResponse)
def actualizar_ahorro(
    id_ahorro: int,
    ahorro: AhorroCreate,
    current_user: object = Depends(get_current_user),
    controller: AhorroController = Depends(get_ahorro_controller),
):
    return controller.actualizar_ahorro(id_ahorro, ahorro, current_user)


@router.delete("/{id_ahorro}")
def eliminar_ahorro(
    id_ahorro: int,
    current_user: object = Depends(get_current_user),
    controller: AhorroController = Depends(get_ahorro_controller),
):
    return controller.eliminar_ahorro(id_ahorro, current_user)
