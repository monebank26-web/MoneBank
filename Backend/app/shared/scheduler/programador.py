import logging
import time

from app.shared.constants.scheduler import (
    SEGUNDOS_ESPERA_BUCLE_SCHEDULER,
    ZONA_HORARIA_SCHEDULER,
)

logger = logging.getLogger(__name__)


class Programador:

    def __init__(self, scheduler=None):
        if scheduler is None:
            from apscheduler.schedulers.background import BackgroundScheduler

            scheduler = BackgroundScheduler(timezone=ZONA_HORARIA_SCHEDULER)
        self.scheduler = scheduler

    def programar_cada(self, job, job_id, minutos):
        self.scheduler.add_job(
            job,
            trigger="interval",
            minutes=minutos,
            id=job_id,
            replace_existing=True,
        )
        return self

    def iniciar(self):
        self.scheduler.start()
        return self

    def detener(self):
        self.scheduler.shutdown(wait=False)

    def esperar(self):
        try:
            while True:
                time.sleep(SEGUNDOS_ESPERA_BUCLE_SCHEDULER)
        except (KeyboardInterrupt, SystemExit):
            logger.info("Scheduler detenido")
