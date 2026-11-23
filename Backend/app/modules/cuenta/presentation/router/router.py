from fastapi import APIRouter, Depends

from app.core.security.auth import get_current_user

from app.modules.cuenta.presentation.controller.cuenta_controller import (
    CuentaController,
    get_cuenta_controller,
)
from app.modules.cuenta.presentation.schema.cuenta_schema import (
    CuentaCreate,
    CuentaResponse,
    CuentaUpdate,
)


router = APIRouter(
    prefix="/cuentas",
    tags=["Cuentas"],
    dependencies=[Depends(get_current_user)]
)


@router.post("/", response_model=CuentaResponse, status_code=201)
def crear_cuenta(
    cuenta: CuentaCreate,
    controller: CuentaController = Depends(get_cuenta_controller),
):
    return controller.crear_cuenta(cuenta)


@router.get("/", response_model=list[CuentaResponse])
def obtener_cuentas(
    usuario_id: int = None,
    controller: CuentaController = Depends(get_cuenta_controller),
    current_user: object = Depends(get_current_user),
):
    return controller.obtener_cuentas(current_user, usuario_id)


@router.get("/{id_cuenta}", response_model=CuentaResponse)
def obtener_cuenta_por_id(
    id_cuenta: int,
    controller: CuentaController = Depends(get_cuenta_controller),
    current_user: object = Depends(get_current_user),
):
    return controller.obtener_cuenta_por_id(id_cuenta, current_user)


@router.put("/{id_cuenta}", response_model=CuentaResponse)
def actualizar_cuenta(
    id_cuenta: int,
    cuenta: CuentaUpdate,
    controller: CuentaController = Depends(get_cuenta_controller),
    current_user: object = Depends(get_current_user),
):
    return controller.actualizar_cuenta(id_cuenta, cuenta, current_user)


@router.delete("/{id_cuenta}")
def eliminar_cuenta(
    id_cuenta: int,
    controller: CuentaController = Depends(get_cuenta_controller),
    current_user: object = Depends(get_current_user),
):
    return controller.eliminar_cuenta(id_cuenta, current_user)
