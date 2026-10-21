from fastapi import APIRouter, Depends

from app.core.security.auth import get_current_user

from app.modules.control_parental.presentation.controller.mesada_controller import (
    MesadaController,
    get_mesada_controller,
)
from app.modules.control_parental.presentation.schema.mesada_parental_schema import (
    MesadaCreate,
    MesadaResponse,
)


router = APIRouter(prefix="/control-parental/dashboard", tags=["Mesadas parentales"])


@router.post("/hijos/{id_hijo}/mesada", response_model=MesadaResponse, status_code=201)
def crear_mesada(
    id_hijo: int,
    data: MesadaCreate,
    current_user=Depends(get_current_user),
    controller: MesadaController = Depends(get_mesada_controller),
):
    return controller.crear_mesada(id_hijo, data, current_user)


@router.get("/hijos/{id_hijo}/mesada", response_model=MesadaResponse | None)
def obtener_mesada(
    id_hijo: int,
    current_user=Depends(get_current_user),
    controller: MesadaController = Depends(get_mesada_controller),
):
    return controller.obtener_mesada(id_hijo, current_user)
