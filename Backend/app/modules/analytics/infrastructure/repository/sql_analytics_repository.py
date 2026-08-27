from datetime import date, timedelta

from sqlalchemy import func, text
from sqlalchemy.orm import Session

from app.modules.analytics.domain.interface.analytics_repository import (
    AnalyticsRepository
)
from app.modules.ahorro.domain.entity.ahorro import Ahorro
from app.modules.ahorro.infrastructure.model.ahorro_model import AhorroModel
from app.modules.ahorro.infrastructure.model.tipo_ahorro_model import (
    TipoAhorroModel
)
from app.modules.cuenta.infrastructure.model.cuenta_model import CuentaModel
from app.modules.transaccion.domain.entity.trans_entity import Transaccion
from app.modules.transaccion.infrastructure.model.categoria_model import (
    CategoriaModel
)
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

    def get_cuenta_usuario(self, id_usuario):
        cuenta = (
            self.db.query(CuentaModel)
            .filter(
                CuentaModel.id_usuario == id_usuario,
                CuentaModel.estado == "ACTIVA",
            )
            .first()
        )
        if not cuenta:
            return None
        return {"id_cuenta": cuenta.id_cuenta, "saldo": cuenta.saldo}

    def get_categoria_nombre(self, id_categoria):
        cat = (
            self.db.query(CategoriaModel)
            .filter(CategoriaModel.id_categoria == id_categoria)
            .first()
        )
        return cat.nombre_categoria if cat else None

    def get_resumen_categoria(self, id_usuario, id_categoria):
        hoy = date.today()
        inicio_mes = hoy.replace(day=1)
        inicio_mes_anterior = (inicio_mes - timedelta(days=1)).replace(day=1)
        fin_mes_anterior = inicio_mes - timedelta(days=1)
        hace_3_meses = hoy - timedelta(days=90)

        gasto_mes = self._sumar_transacciones_categoria(
            id_usuario, id_categoria, inicio_mes, hoy
        )
        gasto_mes_anterior = self._sumar_transacciones_categoria(
            id_usuario, id_categoria, inicio_mes_anterior, fin_mes_anterior
        )
        gasto_3_meses = self._sumar_transacciones_categoria(
            id_usuario, id_categoria, hace_3_meses, hoy
        )
        promedio = gasto_3_meses / 3 if gasto_3_meses else 0

        recientes = (
            self.db.query(HistorialTransaccionModel)
            .filter(
                HistorialTransaccionModel.id_usuario == id_usuario,
                HistorialTransaccionModel.id_categoria == id_categoria,
            )
            .order_by(HistorialTransaccionModel.fecha.desc())
            .limit(3)
            .all()
        )

        transacciones_recientes = []
        for t in recientes:
            fecha_t = t.fecha.date() if hasattr(t.fecha, "date") else t.fecha
            dias = (hoy - fecha_t).days
            if dias <= 0:
                fecha_relativa = "hoy"
            elif dias == 1:
                fecha_relativa = "ayer"
            else:
                fecha_relativa = f"hace {dias} días"
            transacciones_recientes.append({
                "monto": round(float(t.monto)),
                "fecha": fecha_relativa,
            })

        return {
            "gasto_mes": gasto_mes,
            "gasto_mes_anterior": gasto_mes_anterior,
            "promedio_3_meses": promedio,
            "num_transacciones_mes": self._contar_transacciones_categoria(
                id_usuario, id_categoria, inicio_mes, hoy
            ),
            "num_transacciones_mes_anterior": self._contar_transacciones_categoria(
                id_usuario, id_categoria, inicio_mes_anterior, fin_mes_anterior
            ),
            "transacciones_recientes": transacciones_recientes,
        }

    def get_limite_categoria(self, id_usuario, id_categoria):
        cuenta = self.get_cuenta_usuario(id_usuario)
        if not cuenta:
            return None

        tipo_limite = (
            self.db.query(TipoAhorroModel)
            .filter(
                TipoAhorroModel.nombre_tipo_ahorro == Ahorro.TIPO_LIMITE
            )
            .first()
        )
        if not tipo_limite:
            return None

        limite = (
            self.db.query(AhorroModel)
            .filter(
                AhorroModel.id_tipo_ahorro == tipo_limite.id_tipo_ahorro,
                AhorroModel.id_categoria == id_categoria,
                AhorroModel.id_cuenta == cuenta["id_cuenta"],
                AhorroModel.estado == "ACTIVO",
            )
            .first()
        )
        if not limite:
            return None

        rango = Ahorro.calcular_rango_periodo(limite.periodo, date.today())
        if not rango:
            return None

        fecha_desde, fecha_hasta = rango
        gasto_actual = self.db.execute(
            text(
                "SELECT fn_gasto_categoria_periodo("
                ":id_categoria, :id_cuenta, :fecha_desde, :fecha_hasta) AS total"
            ),
            {
                "id_categoria": id_categoria,
                "id_cuenta": cuenta["id_cuenta"],
                "fecha_desde": fecha_desde,
                "fecha_hasta": fecha_hasta,
            },
        ).scalar()

        return {
            "monto_limite": limite.monto_objetivo,
            "gasto_actual": gasto_actual or 0,
            "periodo": limite.periodo,
        }

    def _sumar_transacciones_categoria(
        self, id_usuario, id_categoria, fecha_desde, fecha_hasta
    ):
        total = (
            self.db.query(
                func.coalesce(func.sum(HistorialTransaccionModel.monto), 0)
            )
            .filter(
                HistorialTransaccionModel.id_usuario == id_usuario,
                HistorialTransaccionModel.id_categoria == id_categoria,
                HistorialTransaccionModel.tipo_transaccion == Transaccion.TIPO_GASTO,
                HistorialTransaccionModel.fecha >= fecha_desde,
                HistorialTransaccionModel.fecha <= fecha_hasta,
            )
            .scalar()
        )
        return total or 0

    def _contar_transacciones_categoria(
        self, id_usuario, id_categoria, fecha_desde, fecha_hasta
    ):
        return (
            self.db.query(
                func.count(HistorialTransaccionModel.id_transaccion)
            )
            .filter(
                HistorialTransaccionModel.id_usuario == id_usuario,
                HistorialTransaccionModel.id_categoria == id_categoria,
                HistorialTransaccionModel.tipo_transaccion == Transaccion.TIPO_GASTO,
                HistorialTransaccionModel.fecha >= fecha_desde,
                HistorialTransaccionModel.fecha <= fecha_hasta,
            )
            .scalar()
            or 0
        )
