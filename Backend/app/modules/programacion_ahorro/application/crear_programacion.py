from app.modules.programacion_ahorro.domain.entity.programacion_ahorro import ProgramacionAhorro
from app.shared.exceptions.business_exceptions import (
    CuentaNoEncontrada,
    FrecuenciaInvalida,
    RangoFechasInvalido,
)


class CrearProgramacion:

    def __init__(self, repository, cuenta_repository):
        self.repository = repository
        self.cuenta_repository = cuenta_repository

    def execute(self, programacion_data, id_usuario):
        cuenta = self.cuenta_repository.get_cuenta_por_usuario(id_usuario)

        if not cuenta:
            raise CuentaNoEncontrada()

        programacion = ProgramacionAhorro(
            id_programacion_ahorro=None,
            monto_periodico=programacion_data["monto_periodico"],
            fecha_cobro=programacion_data["fecha_cobro"],
            frecuencia=programacion_data["frecuencia"],
            fecha_inicio=programacion_data["fecha_inicio"],
            fecha_fin=programacion_data.get("fecha_fin"),
            estado=ProgramacionAhorro.ESTADO_ACTIVA,
        )

        if not ProgramacionAhorro.es_frecuencia_valida(programacion.frecuencia):
            raise FrecuenciaInvalida()

        if not ProgramacionAhorro.rango_fechas_valido(
            programacion.fecha_inicio,
            programacion.fecha_fin,
        ):
            raise RangoFechasInvalido()

        return self.repository.create({
            "monto_periodico": programacion.monto_periodico,
            "fecha_cobro": programacion.fecha_cobro,
            "frecuencia": programacion.frecuencia,
            "fecha_inicio": programacion.fecha_inicio,
            "fecha_fin": programacion.fecha_fin,
            "estado": programacion.estado,
        })