from app.shared.exceptions.business_exceptions import (
    CategoriaInvalida,
    CuentaNoEncontrada,
)


class ObtenerConsejoPrevio:

    def __init__(self, analytics_repository, cuenta_repository, consejo_ia_port):
        self.analytics_repository = analytics_repository
        self.cuenta_repository = cuenta_repository
        self.consejo_ia_port = consejo_ia_port

    def execute(self, id_usuario, monto, id_categoria):
        cuenta = self.cuenta_repository.get_cuenta_por_usuario(id_usuario)
        if not cuenta:
            raise CuentaNoEncontrada()

        nombre_categoria = self.analytics_repository.get_categoria_nombre(id_categoria)
        if not nombre_categoria:
            raise CategoriaInvalida()

        stats = self.analytics_repository.calcular_stats_mes(id_usuario)
        resumen_cat = self.analytics_repository.get_resumen_categoria(
            id_usuario, id_categoria
        )
        limite = self.analytics_repository.get_limite_categoria(
            cuenta.id_cuenta, id_categoria
        )

        contexto = {
            "monto": round(float(monto)),
            "categoria": nombre_categoria,
            "saldo_actual": round(float(cuenta.saldo or 0)),
            "saldo_proyectado": round(float(cuenta.saldo or 0) - float(monto)),
            "historial_categoria": {
                "gasto_actual_mes": round(float(resumen_cat["gasto_mes"] or 0)),
                "gasto_mes_anterior": round(
                    float(resumen_cat["gasto_mes_anterior"] or 0)
                ),
                "promedio_3_meses": round(float(resumen_cat["promedio_3_meses"] or 0)),
                "numero_transacciones_mes": resumen_cat["num_transacciones_mes"],
                "numero_transacciones_mes_anterior": resumen_cat[
                    "num_transacciones_mes_anterior"
                ],
                "transacciones_recientes": resumen_cat["transacciones_recientes"],
            },
            "stats_mes": {
                "total_gastado": round(float(stats["total_gastado_mes"] or 0)),
                "total_gastado_proyectado": round(
                    float(stats["total_gastado_mes"] or 0) + float(monto)
                ),
            },
        }

        if limite:
            monto_limite = float(limite["monto_limite"])
            gasto_actual = float(limite["gasto_actual"] or 0)
            contexto["limite"] = {
                "monto_limite": round(monto_limite),
                "porcentaje_usado": (
                    round((gasto_actual / monto_limite) * 100)
                    if monto_limite > 0
                    else 0
                ),
                "porcentaje_proyectado": (
                    round(((gasto_actual + float(monto)) / monto_limite) * 100)
                    if monto_limite > 0
                    else 0
                ),
            }

        return self.consejo_ia_port.generar_consejo(contexto, es_previo=True)
