from datetime import date, timedelta


class ObtenerResumenSemanal:
    def __init__(self, repository):
        self.repository = repository

    def execute(self, id_usuario, fecha_inicio=None, fecha_fin=None):
        if fecha_inicio is None or fecha_fin is None:
            fecha_inicio, fecha_fin = self._calcular_ultima_semana_finalizada()

        movimientos = self.repository.obtener_movimientos_periodo(
            id_usuario, fecha_inicio, fecha_fin
        )

        if not movimientos:
            return {
                "periodo_inicio": fecha_inicio,
                "periodo_fin": fecha_fin,
                "total_ingresos": 0.0,
                "total_gastos": 0.0,
                "balance": 0.0,
                "tiene_movimientos": False,
                "mensaje": "No existen movimientos registrados durante esta semana.",
            }

        total_ingresos = sum(m["total"] for m in movimientos if m["tipo_transaccion"] == "INGRESO")
        total_gastos = sum(m["total"] for m in movimientos if m["tipo_transaccion"] == "GASTO")

        return {
            "periodo_inicio": fecha_inicio,
            "periodo_fin": fecha_fin,
            "total_ingresos": total_ingresos,
            "total_gastos": total_gastos,
            "balance": total_ingresos - total_gastos,
            "tiene_movimientos": True,
            "mensaje": None,
        }

    def _calcular_ultima_semana_finalizada(self):
        hoy = date.today()
        inicio_semana_actual = hoy - timedelta(days=hoy.weekday())
        fin_semana_pasada = inicio_semana_actual - timedelta(days=1)
        inicio_semana_pasada = fin_semana_pasada - timedelta(days=6)
        return inicio_semana_pasada, fin_semana_pasada