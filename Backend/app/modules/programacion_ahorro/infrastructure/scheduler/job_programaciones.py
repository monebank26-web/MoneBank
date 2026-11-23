from app.core.database.uow_factory import abrir_unit_of_work
from app.modules.programacion_ahorro.application.procesar_programaciones_ahorro import (
    ProcesarProgramacionesAhorro,
)
from app.shared.scheduler.reloj import Reloj


def ejecutar_programaciones_ahorro():
    caso_de_uso = ProcesarProgramacionesAhorro(
        abrir_unit_of_work,
        Reloj(),
    )
    return caso_de_uso.execute()
