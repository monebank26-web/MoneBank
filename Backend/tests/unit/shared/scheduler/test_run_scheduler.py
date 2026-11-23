from unittest.mock import Mock

import app.run_scheduler as run_scheduler
from app.core.database.uow_factory import abrir_unit_of_work
from app.modules.programacion_ahorro.infrastructure.scheduler import (
    job_programaciones,
)
from app.shared.constants.scheduler import (
    IDENTIFICADOR_JOB_AHORRO_PROGRAMADO,
    INTERVALO_EJECUCION_AHORRO_PROGRAMADO_MINUTOS,
)
from app.shared.scheduler.reloj import Reloj


def test_main_configura_job_horario(monkeypatch):
    programador = Mock()
    fabrica = Mock(return_value=programador)
    monkeypatch.setattr(run_scheduler, "Programador", fabrica)

    run_scheduler.main()

    fabrica.assert_called_once_with()
    programador.programar_cada.assert_called_once_with(
        run_scheduler.ejecutar_programaciones_ahorro,
        IDENTIFICADOR_JOB_AHORRO_PROGRAMADO,
        INTERVALO_EJECUCION_AHORRO_PROGRAMADO_MINUTOS,
    )
    programador.iniciar.assert_called_once_with()
    programador.esperar.assert_called_once_with()
    programador.detener.assert_called_once_with()


def test_job_delega_en_el_caso_de_uso(monkeypatch):
    caso = Mock()
    caso.execute.return_value = 3
    fabrica = Mock(return_value=caso)
    monkeypatch.setattr(
        job_programaciones,
        "ProcesarProgramacionesAhorro",
        fabrica,
    )

    resultado = job_programaciones.ejecutar_programaciones_ahorro()

    assert resultado == 3
    fabrica.assert_called_once()
    argumentos = fabrica.call_args[0]
    assert argumentos[0] is abrir_unit_of_work
    assert isinstance(argumentos[1], Reloj)
    caso.execute.assert_called_once_with()
