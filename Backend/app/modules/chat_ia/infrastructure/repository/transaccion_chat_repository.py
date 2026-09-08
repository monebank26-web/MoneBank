from datetime import date

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.modules.chat_ia.domain.interface.transaccion_chat_repository import (
    TransaccionChatRepository
)
from app.modules.transaccion.domain.entity.trans_entity import Transaccion
from app.modules.transaccion.infrastructure.model.historial_transaccion_model import (
    HistorialTransaccionModel
)


class SqlTransaccionChatRepository(TransaccionChatRepository):

    def __init__(self, db: Session):
        self.db = db

    def sumar_ingresos(self, id_usuario, desde: date):
        return self._sumar(id_usuario, Transaccion.TIPO_INGRESO, desde)

    def sumar_gastos(self, id_usuario, desde: date):
        return self._sumar(id_usuario, Transaccion.TIPO_GASTO, desde)

    def _sumar(self, id_usuario, tipo, desde):
        total = (
            self.db.query(func.coalesce(func.sum(HistorialTransaccionModel.monto), 0))
            .filter(
                HistorialTransaccionModel.id_usuario == id_usuario,
                HistorialTransaccionModel.tipo_transaccion == tipo,
                HistorialTransaccionModel.fecha >= desde,
            )
            .scalar()
        )
        return total or 0

    def top_categorias(self, id_usuario, desde: date, limite: int):
        filas = (
            self.db.query(
                HistorialTransaccionModel.nombre_categoria.label("nombre_categoria"),
                func.sum(HistorialTransaccionModel.monto).label("total"),
            )
            .filter(
                HistorialTransaccionModel.id_usuario == id_usuario,
                HistorialTransaccionModel.tipo_transaccion == Transaccion.TIPO_GASTO,
                HistorialTransaccionModel.fecha >= desde,
            )
            .group_by(HistorialTransaccionModel.nombre_categoria)
            .order_by(func.sum(HistorialTransaccionModel.monto).desc())
            .limit(limite)
            .all()
        )
        return [
            {
                "nombre_categoria": fila.nombre_categoria,
                "total": fila.total or 0,
            }
            for fila in filas
        ]
