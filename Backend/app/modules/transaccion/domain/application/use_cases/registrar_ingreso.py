from datetime import date

from app.modules.transaccion.domain.entity.trans_entity import Transaccion
from app.modules.transaccion.domain.interface.trans_repository import (
    TransaccionRepository
)
from app.shared.exceptions.business_exceptions import (
    AhorroAsociadoNoValido,
    CategoriaInvalida,
    CuentaNoEncontrada,
    CuentaNoPerteneceAlUsuario,
    FechaInvalida,
    MontoInvalido,
    TipoTransaccionNoValido,
)

class RegistrarIngreso:

    def __init__(self, repository: TransaccionRepository):
        self.repository = repository

    def execute(self, transaccion_data, id_usuario):

        transaccion = Transaccion(
            id=None,
            monto=transaccion_data["monto"],
            tipo=Transaccion.TIPO_INGRESO,
            fecha=transaccion_data["fecha"],
            descripcion=transaccion_data.get("descripcion"),
            categoria=transaccion_data.get("id_categoria"),
        )

        if not transaccion.es_ingreso():
            raise MontoInvalido()

        if transaccion.monto <= 0:
            raise MontoInvalido()

        if not isinstance(transaccion.fecha, date):
            raise FechaInvalida()

        if not self.repository.existe_categoria(
            transaccion.categoria
        ):
            raise CategoriaInvalida()

        cuenta = self.repository.get_cuenta(
            transaccion_data["id_cuenta"]
        )

        if not cuenta:
            raise CuentaNoEncontrada()

        if cuenta.id_usuario != id_usuario:
            raise CuentaNoPerteneceAlUsuario()

        tipo_ingreso = self.repository.get_tipo_transaccion(
                    Transaccion.TIPO_INGRESO
                )
        if not tipo_ingreso:
            raise TipoTransaccionNoValido()

        transaccion_data["id_tipo_transaccion"] = (
            tipo_ingreso.id_tipo_transaccion
        )

        id_ahorro = transaccion_data.get("id_ahorro")

        if id_ahorro:
            ahorro = self.repository.get_ahorro(id_ahorro)

            if not ahorro or ahorro.id_cuenta != cuenta.id_cuenta:
                raise AhorroAsociadoNoValido()
        else:
            transaccion_data["id_ahorro"] = None

        ingreso = self.repository.create(transaccion_data)

        self.repository.aumentar_saldo(
            transaccion_data["id_cuenta"],
            transaccion_data["monto"]
        )

        return ingreso
