from datetime import date

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.modules.analytics.domain.interface.analytics_repository import (
    AnalyticsRepository
)
from app.modules.cuenta.infrastructure.model.cuenta_model import CuentaModel
from app.modules.transaccion.domain.entity.trans_entity import Transaccion
from app.modules.transaccion.infrastructure.model.historial_transaccion_model import (
    HistorialTransaccionModel
)


class SqlAnalyticsRepository(AnalyticsRepository):

    def __init__(self, db: Session):
        self.db = db

    def find_transaccion(self, id_usuario, id_transaccion):
        return (
            self.db.query(HistorialTransaccionModel)
            .filter(
                HistorialTransaccionModel.id_transaccion == id_transaccion,
                HistorialTransaccionModel.id_usuario == id_usuario,
            )
            .first()
        )

    def calcular_stats_mes(self, id_usuario):
        inicio_mes = date.today().replace(day=1)

        filtros = [
            HistorialTransaccionModel.id_usuario == id_usuario,
            HistorialTransaccionModel.tipo_transaccion == Transaccion.TIPO_GASTO,
            HistorialTransaccionModel.fecha >= inicio_mes,
        ]

        total_gastado_mes = (
            self.db.query(func.coalesce(func.sum(HistorialTransaccionModel.monto), 0))
            .filter(*filtros)
            .scalar()
        )

        top_categorias = (
            self.db.query(
                HistorialTransaccionModel.nombre_categoria.label("nombre_categoria"),
                func.sum(HistorialTransaccionModel.monto).label("total"),
            )
            .filter(*filtros)
            .group_by(HistorialTransaccionModel.nombre_categoria)
            .order_by(func.sum(HistorialTransaccionModel.monto).desc())
            .limit(3)
            .all()
        )

        return {
            "total_gastado_mes": total_gastado_mes or 0,
            "top_categorias": [
                {
                    "nombre_categoria": fila.nombre_categoria,
                    "total": fila.total,
                }
                for fila in top_categorias
            ],
        }

    def get_saldo_cuenta(self, id_cuenta):
        cuenta = (
            self.db.query(CuentaModel.saldo)
            .filter(CuentaModel.id_cuenta == id_cuenta)
            .first()
        )
        return cuenta[0] if cuenta else 0
