from datetime import date

from fastapi import Depends, HTTPException
from sqlalchemy.exc import SQLAlchemyError

from app.core.database.unit_of_work import UnitOfWork
from app.core.dependencies.repositories import get_unit_of_work
from app.modules.control_parental.application.use_cases.ejecutar_mesada import (
    EjecutarMesada,
)
from app.modules.control_parental.domain.interface.ejecucion_mesada_repository import (
    EjecucionMesadaRepository,
)


class EjecucionMesadaController:

    def __init__(
        self,
        repository: EjecucionMesadaRepository,
        unit_of_work: UnitOfWork,
    ):
        self.repository = repository
        self.unit_of_work = unit_of_work

    def ejecutar_mesada(self, id_hijo: int, current_user, fecha: date | None = None):
        try:
            ejecucion, proxima = (
                EjecutarMesada(self.repository).execute(
                    current_user.id_usuario,
                    id_hijo,
                    fecha,
                )
            )
            self.unit_of_work.commit()

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
            self.unit_of_work.rollback()

            raise HTTPException(
                status_code=403,
                detail=str(error),
            ) from error

        except ValueError as error:
            self.unit_of_work.rollback()

            raise HTTPException(
                status_code=400,
                detail=str(error),
            ) from error

        except SQLAlchemyError as error:
            self.unit_of_work.rollback()

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


def get_ejecucion_mesada_controller(
    unit_of_work: UnitOfWork = Depends(get_unit_of_work),
) -> EjecucionMesadaController:
    return EjecucionMesadaController(unit_of_work.ejecuciones, unit_of_work)
