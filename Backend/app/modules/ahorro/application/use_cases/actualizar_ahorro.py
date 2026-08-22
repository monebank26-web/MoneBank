from app.modules.ahorro.domain.entity.ahorro import Ahorro
from app.shared.exceptions.business_exceptions import (
    AhorroNoEncontrado,
    CuentaNoEncontrada,
    EstadoInvalido,
    PeriodoInvalido,
    PresupuestoDuplicado,
)

CAMPOS_PERMITIDOS = ("nombre", "monto_objetivo", "estado", "fecha_objetivo", "periodo")


class ActualizarAhorroUseCase:

    def __init__(self, repository):
        self.repository = repository

    def execute(self, id_ahorro, data, id_usuario):

        cuenta = self.repository.get_cuenta_por_usuario(id_usuario)

        if not cuenta:
            raise CuentaNoEncontrada()

        ahorro = self.repository.get_by_id(id_ahorro)

        if not ahorro or ahorro.id_cuenta != cuenta.id_cuenta:
            raise AhorroNoEncontrado()

        data_filtrada = {
            campo: valor for campo, valor in data.items()
            if campo in CAMPOS_PERMITIDOS
        }

        if "estado" in data_filtrada and data_filtrada["estado"] not in (
            Ahorro.ESTADO_ACTIVO,
            Ahorro.ESTADO_PAUSADO,
            Ahorro.ESTADO_FINALIZADO,
        ):
            raise EstadoInvalido()

        tipo_limite = self.repository.get_tipo_ahorro(Ahorro.TIPO_LIMITE)

        if (
            tipo_limite
            and ahorro.id_tipo_ahorro == tipo_limite.id_tipo_ahorro
            and (
                "periodo" in data_filtrada
                or data_filtrada.get("estado") == Ahorro.ESTADO_ACTIVO
            )
        ):
            periodo_resultante = data_filtrada.get("periodo", ahorro.periodo)

            if periodo_resultante and not Ahorro.es_periodo_valido(
                periodo_resultante
            ):
                raise PeriodoInvalido()

            if periodo_resultante:
                existentes = self.repository.get_by_cuenta_y_tipo(
                    cuenta.id_cuenta, Ahorro.TIPO_LIMITE
                )

                duplicado = any(
                    otro.id_ahorro != ahorro.id_ahorro
                    and otro.id_categoria == ahorro.id_categoria
                    and otro.periodo == periodo_resultante
                    and otro.estado == Ahorro.ESTADO_ACTIVO
                    for otro in existentes
                )

                if duplicado:
                    raise PresupuestoDuplicado()

        return self.repository.update(id_ahorro, data_filtrada)
