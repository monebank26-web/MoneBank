import logging

from app.modules.programacion_ahorro.domain.entity.programacion_ahorro import (
    ProgramacionAhorro,
)
from app.modules.transaccion.application.use_cases.registrar_abono_ahorro import (
    RegistrarAbonoAhorro,
)
from app.shared.exceptions.common import SaldoInsuficiente

logger = logging.getLogger(__name__)


class ProcesarProgramacionesAhorro:

    def __init__(
        self,
        abrir_unit_of_work,
        reloj,
        registrar_abono_factory=RegistrarAbonoAhorro,
    ):
        self.abrir_unit_of_work = abrir_unit_of_work
        self.reloj = reloj
        self.registrar_abono_factory = registrar_abono_factory

    def execute(self, hoy=None):
        hoy = hoy or self.reloj.hoy()

        with self.abrir_unit_of_work() as uow:
            vencidas = uow.programaciones.obtener_vencidas(hoy)
            ids = [
                programacion.id_programacion_ahorro
                for programacion in vencidas
            ]

        procesadas = 0
        for programacion_id in ids:
            if self._procesar_una(programacion_id, hoy) is not None:
                procesadas += 1

        return procesadas

    def _procesar_una(self, programacion_id, hoy):
        programacion = None

        try:
            with self.abrir_unit_of_work() as uow:
                modelo = uow.programaciones.get_para_procesar(programacion_id)

                if modelo is None:
                    return None

                programacion = self._a_entidad(modelo)

                if not programacion.esta_vencida(hoy):
                    return None

                ahorro = uow.ahorros.get_by_id(programacion.id_ahorro)

                if ahorro is None:
                    logger.warning(
                        "Programación %s sin meta asociada",
                        programacion_id,
                    )
                    return None

                cuenta = uow.transacciones.get_cuenta(ahorro.id_cuenta)

                if cuenta is None:
                    logger.warning(
                        "Programación %s sin cuenta asociada",
                        programacion_id,
                    )
                    return None

                proxima_fecha = programacion.calcular_proxima_fecha(hoy)
                estado = programacion.siguiente_estado(proxima_fecha)
                descripcion = (
                    "Ahorro programado con fecha esperada a "
                    f"{programacion.fecha_cobro.isoformat()}"
                )

                self.registrar_abono_factory(uow.transacciones).execute(
                    {
                        "id_cuenta": ahorro.id_cuenta,
                        "id_ahorro": ahorro.id_ahorro,
                        "monto": programacion.monto_periodico,
                        "fecha": hoy,
                        "descripcion": descripcion,
                    },
                    cuenta.id_usuario,
                )

                uow.programaciones.actualizar_fecha_cobro(
                    programacion.id_programacion_ahorro,
                    proxima_fecha,
                    estado,
                )
                uow.commit()

                return programacion.id_programacion_ahorro

        except SaldoInsuficiente:
            logger.warning(
                "Saldo insuficiente para la programación %s con fecha %s",
                programacion_id,
                programacion.fecha_cobro if programacion else "desconocida",
            )
            return None
        except Exception:
            logger.exception(
                "Error procesando la programación %s",
                programacion_id,
            )
            return None

    @staticmethod
    def _a_entidad(modelo):
        return ProgramacionAhorro(
            id_programacion_ahorro=modelo.id_programacion_ahorro,
            id_ahorro=modelo.id_ahorro,
            monto_periodico=modelo.monto_periodico,
            fecha_cobro=modelo.fecha_cobro,
            frecuencia=modelo.frecuencia,
            fecha_inicio=modelo.fecha_inicio,
            fecha_fin=modelo.fecha_fin,
            estado=modelo.estado,
        )
