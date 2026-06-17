from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database.connection import get_db

from app.modules.cuenta.presentation.schema.cuenta_schema import (
    CuentaCreate,
    CuentaResponse
)

from app.modules.cuenta.application.use_cases.crear_cuenta import (
    CrearCuenta
)

from app.modules.cuenta.application.use_cases.obtener_cuenta import (
    ObtenerCuentasUseCase
)

from app.modules.cuenta.application.use_cases.obtener_cuenta_por_id import (
    ObtenerCuentaPorIdUseCase
)

from app.modules.cuenta.infrastucture.repository.sql_cuenta_repository import (
    SqlCuentaRepository
)

router = APIRouter(
    prefix="/cuentas",
    tags=["Cuentas"]
)

@router.post("/", response_model=CuentaResponse)
def crear_cuenta(
    cuenta: CuentaCreate,
    db: Session = Depends(get_db)
):

    caso_uso = CrearCuenta()

    return caso_uso.execute(
        db,
        cuenta.model_dump()
    )

@router.get("/")
def obtener_cuentas(
    db: Session = Depends(get_db)
):

    caso_uso = ObtenerCuentasUseCase(
        SqlCuentaRepository()
    )

    return caso_uso.execute(db)

@router.get("/{id_cuenta}")
def obtener_cuenta_por_id(
    id_cuenta: int,
    db: Session = Depends(get_db)
):

    caso_uso = ObtenerCuentaPorIdUseCase(
        SqlCuentaRepository()
    )

    return caso_uso.execute(
        db,
        id_cuenta
    )