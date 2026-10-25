from fastapi import APIRouter, Depends

from app.core.security.auth import get_current_user

from app.modules.programacion_ahorro.presentation.controller.programacion_controller import (
    ProgramacionController,
    get_programacion_controller,
)
from app.modules.programacion_ahorro.presentation.schema.programacion_schema import (
    AhorroAsociadoResponse,
    ProgramacionCreate,
    ProgramacionResponse,
    ProgramacionUpdate,
)


router = APIRouter(
    prefix="/programacion-ahorro",
    tags=["ProgramacionAhorro"],
    dependencies=[Depends(get_current_user)],
)


@router.post("/", response_model=ProgramacionResponse, status_code=201)
def crear_programacion(
    programacion: ProgramacionCreate,
    current_user: object = Depends(get_current_user),
    controller: ProgramacionController = Depends(get_programacion_controller),
):
    return controller.crear_programacion(programacion, current_user)


@router.put("/", response_model=ProgramacionResponse, status_code=200)
def actualizar_estado(
    programacion: ProgramacionUpdate,
    current_user: object = Depends(get_current_user),
    controller: ProgramacionController = Depends(get_programacion_controller),
):
    return controller.actualizar_estado(programacion, current_user)


@router.get("/", response_model=list[AhorroAsociadoResponse], status_code=200)
def consultar_programaciones(
    current_user: object = Depends(get_current_user),
    controller: ProgramacionController = Depends(get_programacion_controller),
):
    return controller.consultar_programaciones(current_user)
