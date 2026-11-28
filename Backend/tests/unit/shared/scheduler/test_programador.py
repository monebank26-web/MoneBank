from datetime import date
from unittest.mock import Mock

from app.shared.constants.scheduler import SEGUNDOS_ESPERA_BUCLE_SCHEDULER
from app.shared.scheduler.programador import Programador
from app.shared.scheduler.reloj import Reloj


def test_reloj_usa_fecha_colombia(monkeypatch):
    esperada = date(2026, 3, 19)
    monkeypatch.setattr(
        "app.shared.scheduler.reloj.hoy_colombia",
        lambda: esperada,
    )

    assert Reloj().hoy() == esperada


def test_programador_configura_job_e_inicia():
    scheduler = Mock()
    job = Mock()
    programador = Programador(scheduler)

    assert programador.programar_cada(job, "job_prueba", 15) is programador

    scheduler.add_job.assert_called_once_with(
        job,
        trigger="interval",
        minutes=15,
        id="job_prueba",
        replace_existing=True,
    )

    programador.iniciar()
    scheduler.start.assert_called_once_with()

    programador.detener()
    scheduler.shutdown.assert_called_once_with(wait=False)


def test_programador_esperar_termina_con_keyboard_interrupt(monkeypatch):
    dormir = Mock(side_effect=KeyboardInterrupt)
    monkeypatch.setattr("app.shared.scheduler.programador.time.sleep", dormir)

    Programador(Mock()).esperar()

    dormir.assert_called_once_with(SEGUNDOS_ESPERA_BUCLE_SCHEDULER)
