from decimal import Decimal

from app.modules.ahorro.domain.entity.ahorro import Ahorro
from app.shared.exceptions.business_exceptions import CuentaNoEncontrada


class ObtenerResumenGlobalMetas:

    def __init__(self, repository, cuenta_repository):
        self.repository = repository
        self.cuenta_repository = cuenta_repository

    def execute(self, id_usuario):

        cuenta = self.cuenta_repository.get_cuenta_por_usuario(id_usuario)

        if not cuenta:
            raise CuentaNoEncontrada()

        metas = self.repository.get_by_cuenta_y_tipo(
            cuenta.id_cuenta,
            Ahorro.TIPO_META,
        )

        total_ahorrado = sum(
            (meta.saldo_actual or 0) for meta in metas
        )
        monto_objetivo_total = sum(
            (meta.monto_objetivo or 0) for meta in metas
        )

        porcentaje_consolidado = (
            (total_ahorrado / monto_objetivo_total) * 100
            if monto_objetivo_total
            else Decimal("0")
        )

        return {
            "total_ahorrado": total_ahorrado,
            "monto_objetivo_total": monto_objetivo_total,
            "porcentaje_consolidado": min(
                porcentaje_consolidado, Decimal("100")
            ),
            "cantidad_metas": len(metas),
        }