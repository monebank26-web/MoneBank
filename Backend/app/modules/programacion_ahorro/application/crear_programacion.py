from app.modules.ahorro.domain.entity.ahorro import Ahorro
from app.modules.programacion_ahorro.domain.entity.programacion_ahorro import ProgramacionAhorro
from app.shared.utils.fechas import es_fecha_posterior_a_hoy
from app.shared.exceptions.ahorro_errors import (
    AhorroNoEncontrado,
    FechaCobroInvalida,
    FrecuenciaInvalida,
    ProgramacionDuplicada,
    RangoFechasInvalido,
)
from app.shared.exceptions.transaccion_errors import (
    AhorroAsociadoNoValido,
    CuentaNoEncontrada,
    CuentaNoPerteneceAlUsuario,
)


class CrearProgramacion:

    def __init__(self, repository, cuenta_repository, ahorro_repository):
        self.repository = repository
        self.cuenta_repository = cuenta_repository
        self.ahorro_repository = ahorro_repository

    def execute(self, programacion_data, id_usuario):
        cuenta = self.cuenta_repository.get_cuenta_por_usuario(id_usuario)

        if not cuenta:
            raise CuentaNoEncontrada()

        ahorro = self.ahorro_repository.get_by_id(programacion_data["id_ahorro"])

        if not ahorro:
            raise AhorroNoEncontrado()

        if ahorro.id_cuenta != cuenta.id_cuenta:
            raise CuentaNoPerteneceAlUsuario()

        tipo_limite = self.ahorro_repository.get_tipo_ahorro(Ahorro.TIPO_LIMITE)

        if tipo_limite and ahorro.id_tipo_ahorro == tipo_limite.id_tipo_ahorro:
            raise AhorroAsociadoNoValido(
                "No se puede programar un aporte a un límite"
            )

        if not ProgramacionAhorro.es_frecuencia_valida(programacion_data["frecuencia"]):
            raise FrecuenciaInvalida()

        if not es_fecha_posterior_a_hoy(programacion_data["fecha_cobro"]):
            raise FechaCobroInvalida()

        if not ProgramacionAhorro.rango_fechas_valido(
            programacion_data["fecha_cobro"],
            programacion_data.get("fecha_fin"),
        ):
            raise RangoFechasInvalido()

        if self.repository.obtener_por_ahorro(programacion_data["id_ahorro"]):
            raise ProgramacionDuplicada()

        programacion = ProgramacionAhorro(
            id_programacion_ahorro=None,
            id_ahorro=programacion_data["id_ahorro"],
            monto_periodico=programacion_data["monto_periodico"],
            fecha_cobro=programacion_data["fecha_cobro"],
            frecuencia=programacion_data["frecuencia"],
            fecha_inicio=programacion_data["fecha_cobro"],
            fecha_fin=programacion_data.get("fecha_fin"),
            estado=ProgramacionAhorro.ESTADO_ACTIVA,
        )

        return self.repository.create({
            "id_ahorro": programacion.id_ahorro,
            "monto_periodico": programacion.monto_periodico,
            "fecha_cobro": programacion.fecha_cobro,
            "frecuencia": programacion.frecuencia,
            "fecha_inicio": programacion.fecha_inicio,
            "fecha_fin": programacion.fecha_fin,
            "estado": programacion.estado,
        })