class Transaccion:

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
        return self.tipo == "INGRESO"

    def es_gasto(self):
        return self.tipo == "GASTO"