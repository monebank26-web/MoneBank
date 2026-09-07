from datetime import date, timedelta


class GenerarReporte:
    def __init__(self, repository):
        self.repository = repository

    def execute(self, id_usuario, periodo=None, fecha_inicio=None, fecha_fin=None):
        if fecha_inicio is None or fecha_fin is None:
            fecha_inicio, fecha_fin = self._calcular_rango(periodo)

        datos = self.repository.obtener_reporte_periodo(id_usuario, fecha_inicio, fecha_fin)

        total_ingresos = sum(
            d["total"] for d in datos if d["tipo_transaccion"] == "INGRESO"
        )
        total_gastos = sum(
            d["total"] for d in datos if d["tipo_transaccion"] == "GASTO"
        )

        return {
            "periodo_inicio": fecha_inicio,
            "periodo_fin": fecha_fin,
            "total_ingresos": total_ingresos,
            "total_gastos": total_gastos,
            "balance": total_ingresos - total_gastos,
            "detalle_por_categoria": datos,
        }

    def _calcular_rango(self, periodo):
        hoy = date.today()
        if periodo == "mensual" or periodo is None:
            inicio_mes_actual = hoy.replace(day=1)
            fecha_fin = inicio_mes_actual - timedelta(days=1)
            fecha_inicio = fecha_fin.replace(day=1)
            return fecha_inicio, fecha_fin
        raise ValueError(f"Periodo no soportado: {periodo}")