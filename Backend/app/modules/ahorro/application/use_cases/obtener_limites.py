from datetime import date
from decimal import Decimal

from app.modules.ahorro.domain.entity.ahorro import Ahorro
from app.shared.exceptions.business_exceptions import CuentaNoEncontrada


def armar_fila_limite(limite, gasto_actual, nombre_categoria=None):

    monto = limite.monto_objetivo or Decimal("0")
    gasto = gasto_actual or Decimal("0")

    porcentaje_usado = (gasto / monto * 100) if monto > 0 else Decimal("0")

    return {
        "id_ahorro": limite.id_ahorro,
        "nombre": limite.nombre,
        "nombre_categoria": nombre_categoria,
        "monto_limite": monto,
        "periodo": limite.periodo,
        "gasto_actual": gasto,
        "porcentaje_usado": porcentaje_usado,
        "monto_disponible": max(monto - gasto, Decimal("0")),
        "estado": limite.estado,
    }


class ObtenerLimites:

    def __init__(self, repository):
        self.repository = repository

    def execute(self, id_usuario):

        cuenta = self.repository.get_cuenta_por_usuario(id_usuario)

        if not cuenta:
            raise CuentaNoEncontrada()

        limites = self.repository.get_by_cuenta_y_tipo(
            cuenta.id_cuenta, Ahorro.TIPO_LIMITE
        )

        resultado = []
        hoy = date.today()

        for limite in limites:
            rango = Ahorro.calcular_rango_periodo(limite.periodo, hoy)

            if not rango:
                continue

            fecha_desde, fecha_hasta = rango

            gasto = self.repository.get_gasto_periodo(
                limite.id_categoria,
                cuenta.id_cuenta,
                fecha_desde,
                fecha_hasta,
            )

            categoria = self.repository.get_categoria(limite.id_categoria)

            resultado.append(armar_fila_limite(
                limite,
                gasto,
                categoria.nombre_categoria if categoria else None,
            ))

        return resultado
