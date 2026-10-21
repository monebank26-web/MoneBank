from fastapi import APIRouter, Depends

from app.core.security.auth import get_current_user

from app.modules.control_parental.presentation.controller.gestionar_mesada_controller import (
    GestionarMesadaController,
    get_gestionar_mesada_controller,
)
from app.modules.control_parental.presentation.schema.mesada_parental_schema import (
    MesadaResponse,
    MesadaUpdate,
)


router = APIRouter(prefix="/control-parental/dashboard", tags=["Gestión de mesadas"])


@router.put("/hijos/{id_hijo}/mesada", response_model=MesadaResponse)
def actualizar_mesada(
    id_hijo: int,
    data: MesadaUpdate,
    current_user=Depends(get_current_user),
    controller: GestionarMesadaController = Depends(get_gestionar_mesada_controller),
):
    return controller.actualizar_mesada(id_hijo, data, current_user)


@router.delete("/hijos/{id_hijo}/mesada", response_model=MesadaResponse)
def cancelar_mesada(
    id_hijo: int,
    current_user=Depends(get_current_user),
    controller: GestionarMesadaController = Depends(get_gestionar_mesada_controller),
):
    return controller.cancelar_mesada(id_hijo, current_user)
