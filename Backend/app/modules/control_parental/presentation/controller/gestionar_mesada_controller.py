from fastapi import Depends, HTTPException

from app.core.database.unit_of_work import UnitOfWork
from app.core.dependencies.repositories import get_unit_of_work
from app.modules.control_parental.application.use_cases.gestionar_mesada import (
    GestionarMesada,
)
from app.modules.control_parental.domain.interface.mesada_parental_repository import (
    MesadaParentalRepository,
)
from app.modules.control_parental.presentation.schema.mesada_parental_schema import (
    MesadaUpdate,
)


def error_http(error):
    if isinstance(error, PermissionError):
        return HTTPException(status_code=403, detail=str(error))
    return HTTPException(status_code=400, detail=str(error))


class GestionarMesadaController:

    def __init__(
        self,
        repository: MesadaParentalRepository,
        unit_of_work: UnitOfWork,
    ):
        self.repository = repository
        self.unit_of_work = unit_of_work

    def actualizar_mesada(
        self,
        id_hijo: int,
        data: MesadaUpdate,
        current_user,
    ):
        try:
            resultado = GestionarMesada(self.repository).actualizar(
                current_user.id_usuario,
                id_hijo,
                data.model_dump(exclude_unset=True),
            )
            self.unit_of_work.commit()
            return resultado
        except (PermissionError, ValueError) as error:
            raise error_http(error) from error

    def cancelar_mesada(self, id_hijo: int, current_user):
        try:
            resultado = GestionarMesada(self.repository).cancelar(
                current_user.id_usuario,
                id_hijo,
            )
            self.unit_of_work.commit()
            return resultado
        except (PermissionError, ValueError) as error:
            raise error_http(error) from error


def get_gestionar_mesada_controller(
    unit_of_work: UnitOfWork = Depends(get_unit_of_work),
) -> GestionarMesadaController:
    return GestionarMesadaController(unit_of_work.mesadas, unit_of_work)
