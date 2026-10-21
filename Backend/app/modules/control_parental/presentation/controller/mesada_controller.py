from fastapi import Depends, HTTPException

from app.core.database.unit_of_work import UnitOfWork
from app.core.dependencies.repositories import get_unit_of_work
from app.modules.control_parental.application.use_cases.configurar_mesada import (
    ConfigurarMesada,
)
from app.modules.control_parental.application.use_cases.obtener_mesada import (
    ObtenerMesada,
)
from app.modules.control_parental.domain.interface.mesada_parental_repository import (
    MesadaParentalRepository,
)
from app.modules.control_parental.presentation.schema.mesada_parental_schema import (
    MesadaCreate,
)


def manejar_error(error):
    raise HTTPException(
        status_code=getattr(error, "status_code", 403),
        detail=getattr(error, "message", str(error)),
    )


class MesadaController:

    def __init__(
        self,
        repository: MesadaParentalRepository,
        unit_of_work: UnitOfWork,
    ):
        self.repository = repository
        self.unit_of_work = unit_of_work

    def crear_mesada(self, id_hijo: int, data: MesadaCreate, current_user):
        try:
            resultado = ConfigurarMesada(self.unit_of_work.mesadas).execute(
                current_user.id_usuario,
                id_hijo,
                data.model_dump(),
            )
            self.unit_of_work.commit()
            return resultado
        except Exception as error:
            manejar_error(error)

    def obtener_mesada(self, id_hijo: int, current_user):
        try:
            return ObtenerMesada(self.repository).execute(
                current_user.id_usuario,
                id_hijo,
            )
        except Exception as error:
            manejar_error(error)


def get_mesada_controller(
    unit_of_work: UnitOfWork = Depends(get_unit_of_work),
) -> MesadaController:
    return MesadaController(unit_of_work.mesadas, unit_of_work)
