from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.modules.cuenta.infrastructure.model.cuenta_model import CuentaModel
from app.modules.transaccion.domain.entity.trans_entity import Transaccion
from app.modules.transaccion.domain.interface.trans_repository import (
    TransaccionRepository
)
from app.modules.transaccion.infrastructure.model.categoria_model import (
    CategoriaModel
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
            .order_by(
                CuentaModel.fecha_creacion.desc()
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

    def create(self, db, transaccion_data):

        transaccion = TransaccionModel(**transaccion_data)

        db.add(transaccion)
        db.commit()
        db.refresh(transaccion)

        return transaccion

    def get_cuenta(self, db, id_cuenta):

        return (
            db.query(CuentaModel)
            .filter(
                CuentaModel.id_cuenta == id_cuenta
            )
            .first()
        )

    def existe_categoria(self, db, id_categoria):

        return (
            db.query(CategoriaModel)
            .filter(
                CategoriaModel.id_categoria == id_categoria
            )
            .first()
            is not None
        )

    def descontar_saldo(self, db, id_cuenta, monto):

        cuenta = self.get_cuenta(
            db,
            id_cuenta
        )

        if not cuenta:
            return None

        cuenta.saldo -= monto

        db.commit()
        db.refresh(cuenta)

        return cuenta
