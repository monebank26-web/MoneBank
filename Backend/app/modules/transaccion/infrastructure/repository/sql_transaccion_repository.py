from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.modules.ahorro.infrastructure.model.ahorro_model import AhorroModel
from app.modules.ahorro.infrastructure.model.tipo_ahorro_model import (
    TipoAhorroModel
)
from app.modules.cuenta.infrastructure.model.cuenta_model import CuentaModel
from app.modules.transaccion.domain.entity.trans_entity import Transaccion
from app.modules.transaccion.domain.interface.trans_repository import (
    TransaccionRepository
)
from app.modules.transaccion.infrastructure.model.categoria_model import (
    CategoriaModel
)
from app.modules.transaccion.infrastructure.model.tipo_transaccion_model import (
    TipoTransaccionModel
)
from app.modules.transaccion.infrastructure.model.transaccion_model import (
    TransaccionModel
)


class SqlTransaccionesRepository(TransaccionRepository):

    def __init__(self, db: Session):
        self.db = db

    def find_by_usuario(self, usuario_id):
        registros = (
            self.db.query(
                TransaccionModel,
                TipoTransaccionModel.nombre_tipo_transaccion
            )
            .join(
                CuentaModel,
                CuentaModel.id_cuenta == TransaccionModel.id_cuenta
            )
            .join(
                TipoTransaccionModel,
                TipoTransaccionModel.id_tipo_transaccion
                == TransaccionModel.id_tipo_transaccion
            )
            .filter(CuentaModel.id_usuario == usuario_id)
            .order_by(TransaccionModel.fecha.desc())
            .all()
        )

        return [
            Transaccion(
                id=registro.id_transaccion,
                monto=registro.monto,
                tipo=nombre_tipo,
                fecha=registro.fecha,
                descripcion=registro.descripcion,
                categoria=registro.id_categoria
            )
            for registro, nombre_tipo in registros
        ]

    def create(self, transaccion_data):
        transaccion = TransaccionModel(**transaccion_data)
        self.db.add(transaccion)
        self.db.commit()
        self.db.refresh(transaccion)
        return transaccion

    def get_cuenta(self, id_cuenta):
        return (
            self.db.query(CuentaModel)
            .filter(CuentaModel.id_cuenta == id_cuenta)
            .first()
        )

    def existe_categoria(self, id_categoria):
        return (
            self.db.query(CategoriaModel)
            .filter(CategoriaModel.id_categoria == id_categoria)
            .first()
            is not None
        )

    def get_tipo_transaccion(self, nombre):
        return (
            self.db.query(TipoTransaccionModel)
            .filter(TipoTransaccionModel.nombre_tipo_transaccion == nombre)
            .first()
        )

    def get_ahorro(self, id_ahorro):
        return (
            self.db.query(AhorroModel)
            .filter(AhorroModel.id_ahorro == id_ahorro)
            .first()
        )

    def descontar_saldo(self, id_cuenta, monto):
        cuenta = self.get_cuenta(id_cuenta)

        if not cuenta:
            return None

        cuenta.saldo -= monto
        self.db.commit()
        self.db.refresh(cuenta)
        return cuenta

    def get_tipo_ahorro(self, nombre):
        return (
            self.db.query(TipoAhorroModel)
            .filter(TipoAhorroModel.nombre_tipo_ahorro == nombre)
            .first()
        )
