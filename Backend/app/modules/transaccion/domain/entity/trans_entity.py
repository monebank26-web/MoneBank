from datetime import date

from app.shared.exceptions.transaccion_errors import (
    FechaInvalida,
    TipoTransaccionNoValido,
)
from app.shared.exceptions.common import MontoInvalido


class Transaccion:

    TIPO_INGRESO = "INGRESO"
    TIPO_GASTO = "GASTO"
    TIPO_AHORRO = "AHORRO"
    TIPO_MOVIMIENTO_AHORRO = "MOVIMIENTO_AHORRO"

    TIPOS_VALIDOS = (
        TIPO_INGRESO,
        TIPO_GASTO,
        TIPO_AHORRO,
        TIPO_MOVIMIENTO_AHORRO,
    )

    def __init__(
        self,
        id,
        monto,
        tipo,
        fecha,
        descripcion,
        categoria
    ):
        self._validar(monto, tipo, fecha)
        self.id = id
        self.monto = monto
        self.tipo = tipo
        self.fecha = fecha
        self.descripcion = descripcion
        self.categoria = categoria

    def _validar(self, monto, tipo, fecha):
        if tipo not in self.TIPOS_VALIDOS:
            raise TipoTransaccionNoValido()
        if monto is None or monto <= 0:
            raise MontoInvalido()
        if not isinstance(fecha, date):
            raise FechaInvalida()

    def es_ingreso(self):
        return self.tipo == self.TIPO_INGRESO

    def es_gasto(self):
        return self.tipo == self.TIPO_GASTO

    def es_ahorro(self):
        return self.tipo == self.TIPO_AHORRO

    def es_movimiento_ahorro(self):
        return self.tipo == self.TIPO_MOVIMIENTO_AHORRO
