from fastapi import APIRouter, Depends, Query

from app.core.security.auth import get_current_user

from app.modules.control_parental.presentation.controller.control_parental_controller import (
    ControlParentalController,
    get_control_parental_controller,
)
from app.modules.control_parental.presentation.schema.control_parental_schema import (
    ConfirmarCodigoRequest,
    HijoParentalResponse,
    PermisoResponse,
    PermisosUpdate,
    RelacionResponse,
    ResumenHijoResponse,
    SolicitarDesvinculacionRequest,
    SolicitarVinculacionRequest,
    SolicitudResponse,
    TransaccionParentalResponse,
)


router = APIRouter(
    prefix="/control-parental",
    tags=["Control parental"],
)


# ============================================================
# VINCULACIÓN
# ============================================================

@router.post(
    "/vinculaciones",
    status_code=201,
)
def solicitar_vinculacion(
    data: SolicitarVinculacionRequest,
    current_user=Depends(get_current_user),
    controller: ControlParentalController = Depends(get_control_parental_controller),
):
    """
    El padre solicita vincular una cuenta hija.
    """
    return controller.solicitar_vinculacion(data, current_user)


@router.post(
    "/vinculaciones/confirmar",
    response_model=RelacionResponse,
)
def confirmar_vinculacion(
    data: ConfirmarCodigoRequest,
    current_user=Depends(get_current_user),
    controller: ControlParentalController = Depends(get_control_parental_controller),
):
    """
    El hijo confirma el código de vinculación.
    """
    return controller.confirmar_vinculacion(data, current_user)


@router.get(
    "/vinculaciones",
    response_model=list[RelacionResponse],
)
def obtener_vinculaciones(
    current_user=Depends(get_current_user),
    controller: ControlParentalController = Depends(get_control_parental_controller),
):
    return controller.obtener_vinculaciones(current_user)


# ============================================================
# DESVINCULACIÓN
# ============================================================

@router.post(
    "/desvinculaciones",
    response_model=SolicitudResponse,
    status_code=201,
)
def solicitar_desvinculacion(
    data: SolicitarDesvinculacionRequest,
    current_user=Depends(get_current_user),
    controller: ControlParentalController = Depends(get_control_parental_controller),
):
    """
    El hijo solicita desvincularse.

    El código se envía al correo del padre,
    pero el hijo lo introduce y confirma.
    """
    return controller.solicitar_desvinculacion(data, current_user)


@router.post(
    "/desvinculaciones/confirmar",
)
def confirmar_desvinculacion(
    data: ConfirmarCodigoRequest,
    current_user=Depends(get_current_user),
    controller: ControlParentalController = Depends(get_control_parental_controller),
):
    """
    El hijo confirma la desvinculación usando el código
    enviado al padre.
    """
    return controller.confirmar_desvinculacion(data, current_user)


# ============================================================
# DASHBOARD DEL PADRE
# ============================================================

@router.get(
    "/dashboard/hijos",
    response_model=list[HijoParentalResponse],
)
def listar_hijos(
    current_user=Depends(get_current_user),
    controller: ControlParentalController = Depends(get_control_parental_controller),
):
    return controller.listar_hijos(current_user)


@router.get(
    "/dashboard/hijos/{id_hijo}/resumen",
    response_model=ResumenHijoResponse,
)
def obtener_resumen_hijo(
    id_hijo: int,
    current_user=Depends(get_current_user),
    controller: ControlParentalController = Depends(get_control_parental_controller),
):
    return controller.obtener_resumen_hijo(id_hijo, current_user)


@router.get(
    "/dashboard/hijos/{id_hijo}/transacciones",
    response_model=list[TransaccionParentalResponse],
)
def obtener_transacciones_hijo(
    id_hijo: int,
    limite: int = Query(
        default=20,
        ge=1,
        le=100,
    ),
    current_user=Depends(get_current_user),
    controller: ControlParentalController = Depends(get_control_parental_controller),
):
    return controller.obtener_transacciones_hijo(id_hijo, limite, current_user)


@router.get(
    "/dashboard/hijos/{id_hijo}/permisos",
    response_model=list[PermisoResponse],
)
def obtener_permisos_hijo(
    id_hijo: int,
    current_user=Depends(get_current_user),
    controller: ControlParentalController = Depends(get_control_parental_controller),
):
    return controller.obtener_permisos_hijo(id_hijo, current_user)


@router.put(
    "/dashboard/hijos/{id_hijo}/permisos",
    response_model=list[PermisoResponse],
)
def actualizar_permisos_hijo(
    id_hijo: int,
    data: PermisosUpdate,
    current_user=Depends(get_current_user),
    controller: ControlParentalController = Depends(get_control_parental_controller),
):
    return controller.actualizar_permisos_hijo(id_hijo, data, current_user)
