from datetime import date

from fastapi import APIRouter, Depends, Query

from app.core.security.auth import get_current_user

from app.modules.control_parental.presentation.controller.ejecucion_mesada_controller import (
    EjecucionMesadaController,
    get_ejecucion_mesada_controller,
)


router = APIRouter(
    prefix="/control-parental/dashboard",
    tags=["Ejecución de mesadas"],
)


@router.post(
    "/hijos/{id_hijo}/mesada/ejecutar"
)
def ejecutar_mesada(
    id_hijo: int,
    fecha: date | None = Query(default=None),
    current_user=Depends(get_current_user),
    controller: EjecucionMesadaController = Depends(get_ejecucion_mesada_controller),
):
    return controller.ejecutar_mesada(id_hijo, current_user, fecha)
