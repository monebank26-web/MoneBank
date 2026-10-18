from typing import List

from fastapi import APIRouter, Depends

from app.core.security.auth import get_current_user

from app.modules.transaccion.presentation.controller.transaccion_controller import (
    TransaccionController,
    get_transaccion_controller,
)
from app.modules.transaccion.presentation.schema.trans_schema import (
    AbonoAhorroRequest,
    CategoriaResponse,
    DetalleTransaccionResponse,
    GastoRequest,
    GastoResponse,
    HistorialPaginadoResponse,
    HistorialRequest,
    TransaccionUpdateRequest,
)


router = APIRouter(
    prefix="/transacciones",
    tags=["Transacciones"]
)


@router.post(
    "/gastos",
    response_model=GastoResponse,
    status_code=201
)
def registrar_gasto(
    gasto: GastoRequest,
    current_user: object = Depends(get_current_user),
    controller: TransaccionController = Depends(get_transaccion_controller),
):
    return controller.registrar_gasto(gasto, current_user)


@router.post(
    "/ingresos",
    response_model=GastoResponse,
    status_code=201
)
def registrar_ingreso(
    ingreso: GastoRequest,
    current_user: object = Depends(get_current_user),
    controller: TransaccionController = Depends(get_transaccion_controller),
):
    return controller.registrar_ingreso(ingreso, current_user)


@router.get("/historial", response_model=HistorialPaginadoResponse, status_code=200)
def obtener_historial(
    current_user: object = Depends(get_current_user),
    controller: TransaccionController = Depends(get_transaccion_controller),
    filtros: HistorialRequest = Depends(),
):
    return controller.obtener_historial(current_user, filtros)


@router.post(
    "/ahorros",
    response_model=GastoResponse,
    status_code=201
)
def registrar_abono_ahorro(
    abono: AbonoAhorroRequest,
    current_user: object = Depends(get_current_user),
    controller: TransaccionController = Depends(get_transaccion_controller),
):
    return controller.registrar_abono_ahorro(abono, current_user)


@router.get("/categorias", response_model=List[CategoriaResponse], status_code=200)
def obtener_categorias(
    current_user: object = Depends(get_current_user),
    controller: TransaccionController = Depends(get_transaccion_controller),
):
    return controller.obtener_categorias(current_user)


@router.get("/{id_transaccion}", response_model=DetalleTransaccionResponse, status_code=200)
def obtener_detalle(
    id_transaccion: int,
    current_user: object = Depends(get_current_user),
    controller: TransaccionController = Depends(get_transaccion_controller),
):
    return controller.obtener_detalle(id_transaccion, current_user)


@router.put("/{id_transaccion}", response_model=GastoResponse, status_code=200)
def actualizar_transaccion(
    id_transaccion: int,
    transaccion: TransaccionUpdateRequest,
    current_user: object = Depends(get_current_user),
    controller: TransaccionController = Depends(get_transaccion_controller),
):
    return controller.actualizar_transaccion(id_transaccion, transaccion, current_user)
