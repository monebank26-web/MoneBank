from datetime import timedelta

from app.core.utils.fechas import hoy_colombia


class GenerarReporte:
    def __init__(self, repository):
        self.repository = repository

    def execute(self, id_usuario, periodo=None, fecha_inicio=None, fecha_fin=None):
        if fecha_inicio is None or fecha_fin is None:
            fecha_inicio, fecha_fin = self._calcular_rango(periodo)

        datos = self.repository.obtener_reporte_periodo(id_usuario, fecha_inicio, fecha_fin)

        detalle_por_categoria = datos["detalle_por_categoria"]

        total_ingresos = sum(
            d["total"] for d in detalle_por_categoria if d["tipo_transaccion"] == "INGRESO"
        )
        total_gastos = sum(
            d["total"] for d in detalle_por_categoria if d["tipo_transaccion"] == "GASTO"
        )

        return {
            "periodo_inicio": fecha_inicio,
            "periodo_fin": fecha_fin,
            "total_ingresos": total_ingresos,
            "total_gastos": total_gastos,
            "balance": total_ingresos - total_gastos,
            "total_metas": datos.get("total_metas", 0),
            "detalle_por_categoria": detalle_por_categoria,
        }

    def _calcular_rango(self, periodo):
        hoy = hoy_colombia()
        if periodo == "mensual" or periodo is None:
            inicio_mes_actual = hoy.replace(day=1)
            fecha_fin = inicio_mes_actual - timedelta(days=1)
            fecha_inicio = fecha_fin.replace(day=1)
            return fecha_inicio, fecha_fin
        raise ValueError(f"Periodo no soportado: {periodo}")