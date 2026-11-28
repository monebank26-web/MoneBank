from fastapi import Depends

from app.core.database.unit_of_work import UnitOfWork
from app.core.dependencies.repositories import get_unit_of_work
from app.modules.programacion_ahorro.application.actualizar_estado import (
    ActualizarEstadoUseCase,
)
from app.modules.programacion_ahorro.application.consultar_programaciones import (
    ConsultarProgramacionesUseCase,
)
from app.modules.programacion_ahorro.application.crear_programacion import (
    CrearProgramacion,
)
from app.modules.programacion_ahorro.application.modificar_programacion import (
    ModificarProgramacion,
)
from app.modules.programacion_ahorro.domain.interface.programacion_repository import (
    ProgramacionAhorroRepository,
)
from app.modules.programacion_ahorro.presentation.schema.programacion_schema import (
    CambiarEstadoRequest,
    ModificarProgramacionRequest,
    ProgramacionCreate,
)


class ProgramacionController:

    def __init__(
        self,
        repository: ProgramacionAhorroRepository,
        unit_of_work: UnitOfWork,
    ):
        self.repository = repository
        self.unit_of_work = unit_of_work

    def crear_programacion(
        self,
        programacion: ProgramacionCreate,
        current_user,
    ):
        caso_uso = CrearProgramacion(
            self.repository,
            self.unit_of_work.cuentas,
            self.unit_of_work.ahorros,
        )
        resultado = caso_uso.execute(
            programacion.model_dump(),
            current_user.id_usuario,
        )
        self.unit_of_work.commit()
        return resultado

    def actualizar_estado(
        self,
        id_programacion_ahorro: int,
        data: CambiarEstadoRequest,
        current_user,
    ):
        caso_uso = ActualizarEstadoUseCase(
            self.repository,
            self.unit_of_work.cuentas,
            self.unit_of_work.ahorros,
        )
        resultado = caso_uso.execute(
            current_user.id_usuario,
            id_programacion_ahorro,
            data.estado,
        )
        self.unit_of_work.commit()
        return resultado

    def modificar_programacion(
        self,
        id_programacion_ahorro: int,
        data: ModificarProgramacionRequest,
        current_user,
    ):
        caso_uso = ModificarProgramacion(
            self.repository,
            self.unit_of_work.cuentas,
            self.unit_of_work.ahorros,
        )
        resultado = caso_uso.execute(
            current_user.id_usuario,
            id_programacion_ahorro,
            data.monto_periodico,
            data.frecuencia,
        )
        self.unit_of_work.commit()
        return resultado

    def consultar_programaciones(self, current_user):
        caso_uso = ConsultarProgramacionesUseCase(
            self.repository,
            self.unit_of_work.cuentas,
        )
        return caso_uso.execute(current_user.id_usuario)


def get_programacion_controller(
    unit_of_work: UnitOfWork = Depends(get_unit_of_work),
) -> ProgramacionController:
    return ProgramacionController(unit_of_work.programaciones, unit_of_work)
