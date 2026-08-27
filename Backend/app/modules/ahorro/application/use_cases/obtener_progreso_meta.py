from app.modules.ahorro.domain.entity.ahorro import Ahorro
from app.shared.exceptions.business_exceptions import (
    CuentaNoEncontrada,
    MetaNoEncontrada,
)


class ObtenerProgresoMeta:

    def __init__(self, repository):
        self.repository = repository

    def execute(self, id_ahorro, id_usuario):

        cuenta = self.repository.get_cuenta_por_usuario(id_usuario)

        if not cuenta:
            raise CuentaNoEncontrada()

        ahorro = self.repository.get_by_id(id_ahorro)

        if not ahorro or ahorro.id_cuenta != cuenta.id_cuenta:
            raise MetaNoEncontrada()

        tipo_meta = self.repository.get_tipo_ahorro(Ahorro.TIPO_META)

        if ahorro.id_tipo_ahorro != tipo_meta.id_tipo_ahorro:
            raise MetaNoEncontrada()

        progreso = self.repository.get_progreso(id_ahorro)

        return {
            "id_meta": ahorro.id_ahorro,
            "nombre": ahorro.nombre,
            "monto_objetivo": ahorro.monto_objetivo,
            "monto_acumulado": ahorro.saldo_actual,
            "porcentaje_avance": progreso["porcentaje_avance"],
            "monto_faltante": progreso["monto_faltante"],
        }
