from datetime import date

from app.modules.transaccion.domain.entity.trans_entity import Transaccion
from app.modules.transaccion.domain.interface.trans_repository import (
    TransaccionRepository
)
from app.shared.exceptions.transaccion import (
    CategoriaInvalida,
    CuentaNoEncontrada,
    CuentaNoPerteneceAlUsuario,
    FechaInvalida,
    MontoInvalido,
)


class RegistrarGasto:

    def __init__(self, repository: TransaccionRepository):
        self.repository = repository

    def execute(self, db, transaccion_data, id_usuario):

        transaccion = Transaccion(
            id=None,
            monto=transaccion_data["monto"],
            tipo=Transaccion.TIPO_GASTO,
            fecha=transaccion_data["fecha"],
            descripcion=transaccion_data.get("descripcion"),
            categoria=transaccion_data.get("id_categoria"),
        )

        if not transaccion.es_gasto():
            raise MontoInvalido()

        if transaccion.monto <= 0:
            raise MontoInvalido()

        if not isinstance(transaccion.fecha, date):
            raise FechaInvalida()

        if not self.repository.existe_categoria(
            db,
            transaccion.categoria
        ):
            raise CategoriaInvalida()

        cuenta = self.repository.get_cuenta(
            db,
            transaccion_data["id_cuenta"]
        )

        if not cuenta:
            raise CuentaNoEncontrada()

        if cuenta.id_usuario != id_usuario:
            raise CuentaNoPerteneceAlUsuario()

        transaccion_data["tipo"] = Transaccion.TIPO_GASTO

        gasto = self.repository.create(
            db,
            transaccion_data
        )

        self.repository.descontar_saldo(
            db,
            transaccion_data["id_cuenta"],
            transaccion_data["monto"]
        )

        return gasto
