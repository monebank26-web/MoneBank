from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.database.connection import get_db
from app.core.security.auth import get_current_user

from app.modules.control_parental.application.use_cases.ejecutar_mesada import (
    EjecutarMesada,
)

from app.modules.control_parental.infrastructure.repository.sql_ejecucion_mesada_repository import (
    SqlEjecucionMesadaRepository,
)


router = APIRouter(
    prefix="/control-parental/dashboard",
    tags=["Ejecución de mesadas"],
)


def get_repository(
    db: Session = Depends(get_db),
):
    return SqlEjecucionMesadaRepository(db)


@router.post(
    "/hijos/{id_hijo}/mesada/ejecutar"
)
def ejecutar_mesada(
    id_hijo: int,
    fecha: date | None = Query(default=None),
    current_user=Depends(get_current_user),
    repository=Depends(get_repository),
):
    try:
        ejecucion, proxima = (
            EjecutarMesada(repository).execute(
                current_user.id_usuario,
                id_hijo,
                fecha,
            )
        )

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
        repository.rollback()

        raise HTTPException(
            status_code=403,
            detail=str(error),
        ) from error

    except ValueError as error:
        repository.rollback()

        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error

    except SQLAlchemyError as error:
        repository.rollback()

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
