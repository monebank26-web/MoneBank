from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database.connection import get_db
from app.core.security.auth import get_current_user

from app.modules.transaccion.application.use_cases.obtener_transacciones import (
    ObtenerTransaccionesUseCase
)

from app.modules.transaccion.application.use_cases.registrar_gasto import (
    RegistrarGasto
)

from app.modules.transaccion.domain.interface.trans_repository import (
    TransaccionRepository
)

from app.modules.transaccion.infrastructure.repository.sql_transaccion_repository import (
    SqlTransaccionesRepository
)

from app.modules.transaccion.presentation.schema.trans_schema import (
    GastoRequest,
    GastoResponse,
    ListaTransaccionesResponse
)

from app.shared.exceptions.transaccion import (
    CategoriaInvalida,
    CuentaNoEncontrada,
    CuentaNoPerteneceAlUsuario,
    FechaInvalida,
    MontoInvalido,
    TransaccionesNoEncontrado,
)


router = APIRouter(
    prefix="/transacciones",
    tags=["Transacciones"]
)


def get_transaccion_repository(
    db: Session = Depends(get_db)
) -> TransaccionRepository:
    return SqlTransaccionesRepository(db)


@router.post(
    "/gastos",
    response_model=GastoResponse,
    status_code=201
)
def registrar_gasto(
    gasto: GastoRequest,
    db: Session = Depends(get_db),
    current_user: object = Depends(get_current_user),
    repository: TransaccionRepository = Depends(get_transaccion_repository)
):
    caso_uso = RegistrarGasto(repository)

    try:
        return caso_uso.execute(
            db,
            gasto.model_dump(),
            current_user.id_usuario
        )

    except HTTPException:
        raise

    except MontoInvalido:
        raise HTTPException(
            status_code=400,
            detail="El monto del gasto debe ser mayor a 0"
        )

    except FechaInvalida:
        raise HTTPException(
            status_code=400,
            detail="La fecha del gasto no es válida"
        )

    except CategoriaInvalida:
        raise HTTPException(
            status_code=422,
            detail="La categoría no existe en el catálogo"
        )

    except CuentaNoEncontrada:
        raise HTTPException(
            status_code=404,
            detail="Cuenta no encontrada"
        )

    except CuentaNoPerteneceAlUsuario:
        raise HTTPException(
            status_code=403,
            detail="La cuenta no pertenece al usuario autenticado"
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Error interno al registrar el gasto"
        )


@router.get(
    "/",
    response_model=List[ListaTransaccionesResponse],
    status_code=200
)
def obtener_transacciones(
    current_user: object = Depends(get_current_user),
    repository: TransaccionRepository = Depends(get_transaccion_repository)
):
    caso_uso = ObtenerTransaccionesUseCase(repository)

    try:
        return caso_uso.execute(current_user.id_usuario)

    except TransaccionesNoEncontrado:
        raise HTTPException(
            status_code=404,
            detail="No se encontraron transacciones"
        )
