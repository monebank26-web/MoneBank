from datetime import date

from app.modules.ahorro.domain.entity.ahorro import Ahorro
from app.modules.transaccion.domain.entity.trans_entity import Transaccion
from app.modules.transaccion.domain.interface.trans_repository import (
    TransaccionRepository
)
from app.shared.exceptions.business_exceptions import (
    AhorroAsociadoNoValido,
    CuentaNoEncontrada,
    CuentaNoPerteneceAlUsuario,
    FechaInvalida,
    MontoInvalido,
    SaldoInsuficiente,
    TipoTransaccionNoValido,
)


class RegistrarAbonoAhorro:

    def __init__(self, repository: TransaccionRepository):
        self.repository = repository

    def execute(self, transaccion_data, id_usuario):

        if transaccion_data["monto"] <= 0:
            raise MontoInvalido()

        if not isinstance(transaccion_data["fecha"], date):
            raise FechaInvalida()

        cuenta = self.repository.get_cuenta(
            transaccion_data["id_cuenta"]
        )

        if not cuenta:
            raise CuentaNoEncontrada()

        if cuenta.id_usuario != id_usuario:
            raise CuentaNoPerteneceAlUsuario()

        ahorro = self.repository.get_ahorro(
            transaccion_data["id_ahorro"]
        )

        if not ahorro or ahorro.id_cuenta != cuenta.id_cuenta:
            raise AhorroAsociadoNoValido()

        tipo_limite = self.repository.get_tipo_ahorro(Ahorro.TIPO_LIMITE)

        if tipo_limite and ahorro.id_tipo_ahorro == tipo_limite.id_tipo_ahorro:
            raise AhorroAsociadoNoValido(
                "No se puede abonar a un límite de gasto"
            )

        tipo_movimiento = self.repository.get_tipo_transaccion(
            Transaccion.TIPO_MOVIMIENTO_AHORRO
        )

        if not tipo_movimiento:
            raise TipoTransaccionNoValido(
                f"El tipo {Transaccion.TIPO_MOVIMIENTO_AHORRO} "
                "no existe en el catálogo"
            )

        if transaccion_data["monto"] > cuenta.saldo:
            raise SaldoInsuficiente()

        abono_creado = self.repository.create({
            "monto": transaccion_data["monto"],
            "fecha": transaccion_data["fecha"],
            "descripcion": transaccion_data.get("descripcion"),
            "id_tipo_transaccion": tipo_movimiento.id_tipo_transaccion,
            "id_cuenta": cuenta.id_cuenta,
            "id_categoria": ahorro.id_categoria,
            "id_ahorro": ahorro.id_ahorro,
        })

        self.repository.descontar_saldo(cuenta.id_cuenta, transaccion_data["monto"])
        self.repository.sumar_saldo_ahorro(ahorro.id_ahorro, transaccion_data["monto"])

        return abono_creado
