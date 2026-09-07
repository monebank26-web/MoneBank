from datetime import date

from app.modules.ahorro.domain.entity.ahorro import Ahorro
from app.shared.exceptions.business_exceptions import CuentaNoEncontrada


class ObtenerAlertasPresupuesto:

    def __init__(self, repository, cuenta_repository):
        self.repository = repository
        self.cuenta_repository = cuenta_repository

    def execute(self, id_usuario):

        cuenta = self.cuenta_repository.get_cuenta_por_usuario(id_usuario)

        if not cuenta:
            raise CuentaNoEncontrada()

        limites = self.repository.get_by_cuenta_y_tipo(
            cuenta.id_cuenta, Ahorro.TIPO_LIMITE
        )

        alertas = []
        hoy = date.today()

        for limite in limites:

            if limite.estado != Ahorro.ESTADO_ACTIVO or not limite.monto_objetivo:
                continue

            rango = Ahorro.calcular_rango_periodo(limite.periodo, hoy)

            if not rango:
                continue

            fecha_desde, fecha_hasta = rango

            gasto = self.repository.get_gasto_periodo(
                limite.id_categoria,
                cuenta.id_cuenta,
                fecha_desde,
                fecha_hasta,
            ) or 0

            porcentaje_usado = gasto / limite.monto_objetivo * 100

            if porcentaje_usado < Ahorro.UMBRAL_ALERTA:
                continue

            superado = porcentaje_usado > 100

            alertas.append({
                "tipo_alerta": (
                    "LIMITE_SUPERADO" if superado else "PREVENTIVA"
                ),
                "mensaje": (
                    f"Has superado el límite de '{limite.nombre}': "
                    f"llevas {porcentaje_usado:.0f}% del presupuesto"
                    if superado
                    else
                    f"Estás cerca del límite de '{limite.nombre}': "
                    f"llevas {porcentaje_usado:.0f}% del presupuesto"
                ),
                "fecha": hoy,
            })

        return alertas
