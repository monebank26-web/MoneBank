class Transaccion:

    TIPO_INGRESO = "INGRESO"
    TIPO_GASTO = "GASTO"
    TIPO_AHORRO = "AHORRO"
    TIPO_MOVIMIENTO_AHORRO = "MOVIMIENTO_AHORRO"

    def __init__(
        self,
        id,
        monto,
        tipo,
        fecha,
        descripcion,
        categoria
    ):
        self.id = id
        self.monto = monto
        self.tipo = tipo
        self.fecha = fecha
        self.descripcion = descripcion
        self.categoria = categoria

    def es_ingreso(self):
        return self.tipo == self.TIPO_INGRESO

    def es_gasto(self):
        return self.tipo == self.TIPO_GASTO

    def es_ahorro(self):
        return self.tipo == self.TIPO_AHORRO
