from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.exc import SQLAlchemyError

from app.core.database.unit_of_work import UnitOfWork
from app.core.dependencies.repositories import get_unit_of_work
from app.core.security.auth import get_current_user

from app.modules.control_parental.application.use_cases.ejecutar_mesada import (
    EjecutarMesada,
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
    unit_of_work: UnitOfWork = Depends(get_unit_of_work),
):
    try:
        ejecucion, proxima = (
            EjecutarMesada(unit_of_work.ejecuciones).execute(
                current_user.id_usuario,
                id_hijo,
                fecha,
            )
        )
        unit_of_work.commit()

        return {
            "mensaje": (
                "Mesada ejecutada correctamente"
            ),
            "id_ejecucion": ejecucion.id_ejecucion,
            "id_mesada": ejecucion.id_mesada,
            "monto": ejecucion.monto,
            "periodo": ejecucion.periodo,
            "id_transaccion_salida": (
                ejecucion.id_transaccion_salida
            ),
            "id_transaccion_entrada": (
                ejecucion.id_transaccion_entrada
            ),
            "proxima_ejecucion": proxima,
            "estado": ejecucion.estado,
        }

    except PermissionError as error:
        unit_of_work.rollback()

        raise HTTPException(
            status_code=403,
            detail=str(error),
        ) from error

    except ValueError as error:
        unit_of_work.rollback()

        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error

    except SQLAlchemyError as error:
        unit_of_work.rollback()

        print(
            "ERROR REAL AL EJECUTAR MESADA:",
            repr(error),
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "Error de base de datos al crear "
                "las transacciones de la mesada"
            ),
        ) from error
