class ProgramacionDetalle:

    ESTADO_ACTIVA = "ACTIVA"

    def __init__(
        self,
        id_programacion_ahorro,
        id_ahorro,
        nombre_ahorro,
        monto_periodico,
        fecha_cobro,
        frecuencia,
        fecha_inicio,
        fecha_fin,
        tiempo_restante,
        estado
    ):
        self.id_programacion_ahorro = id_programacion_ahorro
        self.id_ahorro = id_ahorro
        self.nombre_ahorro = nombre_ahorro
        self.monto_periodico = monto_periodico
        self.fecha_cobro = fecha_cobro
        self.frecuencia = frecuencia
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.tiempo_restante = tiempo_restante
        self.estado = estado

    @classmethod
    def tiempo_restante_de(cls, dias):
        if dias is None or dias < 0:
            return None
        if dias == 0:
            return "Hoy"
        if dias == 1:
            return "En 1 día"
        return "En {0} días".format(dias)

    @classmethod
    def desde_fila(cls, fila):
        dias = fila.dias_para_proximo_cobro
        ocultar_cobro = (
            fila.estado_programacion != cls.ESTADO_ACTIVA
            or dias is None
            or dias < 0
        )

        return cls(
            id_programacion_ahorro=fila.id_programacion_ahorro,
            id_ahorro=fila.id_ahorro,
            nombre_ahorro=fila.nombre_ahorro,
            monto_periodico=fila.monto_periodico,
            fecha_cobro=None if ocultar_cobro else fila.proxima_fecha_cobro,
            frecuencia=fila.frecuencia,
            fecha_inicio=fila.fecha_inicio_vigencia,
            fecha_fin=fila.fecha_fin_vigencia,
            tiempo_restante=(
                None if ocultar_cobro else cls.tiempo_restante_de(dias)
            ),
            estado=fila.estado_programacion,
        )