from app.modules.transaccion.domain.entity.trans_entity import Transaccion
from app.modules.transaccion.domain.interface.trans_repository import (
    TransaccionRepository
)
from app.shared.exceptions.business_exceptions import (
    CategoriaInvalida,
    CuentaNoEncontrada,
    CuentaNoPerteneceAlUsuario,
    MontoInvalido,
    SaldoInsuficiente,
    TransaccionNoEditable,
    TransaccionesNoEncontrado,
)


class ActualizarTransaccion:

    def __init__(self, repository: TransaccionRepository):
        self.repository = repository

    def execute(self, id_transaccion, datos, id_usuario):

        transaccion = self.repository.get_transaccion(id_transaccion)

        if not transaccion:
            raise TransaccionesNoEncontrado()

        cuenta = self.repository.get_cuenta(transaccion.id_cuenta)

        if not cuenta:
            raise CuentaNoEncontrada()

        if cuenta.id_usuario != id_usuario:
            raise CuentaNoPerteneceAlUsuario()

        tipo_gasto = self.repository.get_tipo_transaccion(
            Transaccion.TIPO_GASTO
        )
        tipo_ingreso = self.repository.get_tipo_transaccion(
            Transaccion.TIPO_INGRESO
        )

        es_gasto = (
            tipo_gasto is not None
            and transaccion.id_tipo_transaccion == tipo_gasto.id_tipo_transaccion
        )
        es_ingreso = (
            tipo_ingreso is not None
            and transaccion.id_tipo_transaccion == tipo_ingreso.id_tipo_transaccion
        )

        if not es_gasto and not es_ingreso:
            raise TransaccionNoEditable(
                "Solo se pueden editar gastos e ingresos"
            )

        if transaccion.estado and transaccion.estado.upper() == "CANCELADA":
            raise TransaccionNoEditable(
                "No se puede editar una transacción cancelada"
            )

        monto_nuevo = datos["monto"]

        if monto_nuevo is None or monto_nuevo <= 0:
            raise MontoInvalido()

        if not self.repository.existe_categoria(datos.get("id_categoria")):
            raise CategoriaInvalida()

        monto_actual = transaccion.monto

        if es_gasto:
            nuevo_saldo = cuenta.saldo + monto_actual - monto_nuevo

            if nuevo_saldo < 0:
                raise SaldoInsuficiente()
        else:
            nuevo_saldo = cuenta.saldo - monto_actual + monto_nuevo

        return self.repository.update_transaccion(
            transaccion,
            datos,
            cuenta.id_cuenta,
            nuevo_saldo
        )
