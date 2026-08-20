from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database.connection import get_db
from app.core.security.auth import get_current_user
from app.core.security.roles import ROL_ADMIN

from app.modules.cuenta.presentation.schema.cuenta_schema import (
    CuentaCreate,
    CuentaResponse
)

from app.modules.cuenta.application.use_cases.crear_cuenta import CrearCuenta
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
    usuario_id: int = None,
    repository: CuentaRepository = Depends(get_cuenta_repository),
    current_user: object = Depends(get_current_user),
):
    if current_user.id_rol == ROL_ADMIN:
        if usuario_id:
            caso_uso = ObtenerCuentaPorIdUseCase(repository)
            resultado = caso_uso.execute(usuario_id)
            if not resultado["success"]:
                raise HTTPException(status_code=404, detail="Cuenta no encontrada")
            return [resultado["cuenta"]]
        return repository.get_all()
    else:
        caso_uso = ObtenerCuentaPorIdUseCase(repository)
        resultado = caso_uso.execute(current_user.id_usuario)
        if not resultado["success"]:
            raise HTTPException(status_code=404, detail="Cuenta no encontrada")
        return [resultado["cuenta"]]


@router.delete("/{id_cuenta}")
def eliminar_cuenta(
    id_cuenta: int,
    repository: CuentaRepository = Depends(get_cuenta_repository),
    current_user: object = Depends(get_current_user),
):
    cuenta = repository.get_by_id_cuenta(id_cuenta)
    if not cuenta:
        raise HTTPException(status_code=404, detail="Cuenta no encontrada")
    if current_user.id_rol != ROL_ADMIN and cuenta.id_usuario != current_user.id_usuario:
        raise HTTPException(status_code=403, detail="No puedes eliminar esta cuenta")
    return repository.delete(id_cuenta)
