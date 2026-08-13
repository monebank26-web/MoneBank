from sqlalchemy.orm import Session

from app.modules.cuenta.infrastructure.model.cuenta_model import CuentaModel
from app.modules.transaccion.domain.entity.trans_entity import Transaccion
from app.modules.transaccion.domain.interface.trans_repository import (
    TransaccionRepository
)
from app.modules.transaccion.infrastructure.model.transaccion_model import (
    TransaccionModel
)


class SqlTransaccionesRepository(TransaccionRepository):

    def __init__(self, db: Session):
        self.db = db

    def find_by_usuario(self, usuario_id):

        registros = (
            self.db.query(TransaccionModel)
            .join(
                CuentaModel,
                CuentaModel.id_cuenta == TransaccionModel.id_cuenta
            )
            .filter(
                CuentaModel.id_usuario == usuario_id
            )
            .all()
        )

        return [
            Transaccion(
                id=registro.id_transaccion,
                monto=registro.monto,
                tipo=registro.tipo,
                fecha=registro.fecha,
                descripcion=registro.descripcion,
                categoria=registro.id_categoria
            )
            for registro in registros
        ]
