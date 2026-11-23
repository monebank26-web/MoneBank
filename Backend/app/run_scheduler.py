import logging

from app.modules.programacion_ahorro.infrastructure.scheduler.job_programaciones import (
    ejecutar_programaciones_ahorro,
)
from app.shared.constants.scheduler import (
    IDENTIFICADOR_JOB_AHORRO_PROGRAMADO,
    INTERVALO_EJECUCION_AHORRO_PROGRAMADO_MINUTOS,
)
from app.shared.scheduler.programador import Programador

logger = logging.getLogger(__name__)


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )

    programador = Programador()
    programador.programar_cada(
        ejecutar_programaciones_ahorro,
        IDENTIFICADOR_JOB_AHORRO_PROGRAMADO,
        INTERVALO_EJECUCION_AHORRO_PROGRAMADO_MINUTOS,
    )
    programador.iniciar()

    logger.info(
        "Scheduler de ahorro programado iniciado cada %s minutos",
        INTERVALO_EJECUCION_AHORRO_PROGRAMADO_MINUTOS,
    )

    try:
        programador.esperar()
    finally:
        programador.detener()


if __name__ == "__main__":
    main()
