from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database.connection import get_db
from app.core.security.auth import get_current_user

from app.modules.cuenta.presentation.schema.cuenta_schema import (
    CuentaCreate,
    CuentaResponse
)

from app.modules.cuenta.application.use_cases.crear_cuenta import CrearCuenta
from app.modules.cuenta.application.use_cases.obtener_cuenta import ObtenerCuentasUseCase
from app.modules.cuenta.application.use_cases.obtener_cuenta_por_id import ObtenerCuentaPorIdUseCase

from app.modules.cuenta.domain.interface.cuenta_repository import CuentaRepository
from app.modules.cuenta.infrastructure.repository.sql_cuenta_repository import SqlCuentaRepository


router = APIRouter(
    prefix="/cuentas",
    tags=["Cuentas"],
    dependencies=[Depends(get_current_user)]
)


def get_cuenta_repository(
    db: Session = Depends(get_db)
) -> CuentaRepository:
    return SqlCuentaRepository(db)


@router.post("/", response_model=CuentaResponse)
def crear_cuenta(
    cuenta: CuentaCreate,
    repository: CuentaRepository = Depends(get_cuenta_repository),
):
    caso_uso = CrearCuenta(repository)
    return caso_uso.execute(cuenta.model_dump())


@router.get("/")
def obtener_cuentas(
    repository: CuentaRepository = Depends(get_cuenta_repository),
):
    caso_uso = ObtenerCuentasUseCase(repository)
    return caso_uso.execute()


@router.get("/{id_cuenta}")
def obtener_cuenta_por_id(
    id_cuenta: int,
    repository: CuentaRepository = Depends(get_cuenta_repository),
):
    caso_uso = ObtenerCuentaPorIdUseCase(repository)
    return caso_uso.execute(id_cuenta)
