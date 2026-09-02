from datetime import date


class ProgramacionAhorro:

    PERIODO_DIARIA = "DIARIA"
    PERIODO_SEMANAL = "SEMANAL"
    PERIODO_QUINCENAL = "QUINCENAL"
    PERIODO_MENSUAL = "MENSUAL"
    PERIODO_TRIMESTRAL = "TRIMESTRAL"
    PERIODO_SEMESTRAL = "SEMESTRAL"
    PERIODO_ANUAL = "ANUAL"

    PERIODOS_VALIDOS = (
        PERIODO_DIARIA,
        PERIODO_SEMANAL,
        PERIODO_QUINCENAL,
        PERIODO_MENSUAL,
        PERIODO_TRIMESTRAL,
        PERIODO_SEMESTRAL,
        PERIODO_ANUAL,
    )

    ESTADO_ACTIVA = "ACTIVA"
    ESTADO_PAUSADA = "PAUSADA"
    ESTADO_FINALIZADA = "FINALIZADA"

    ESTADOS_VALIDOS = (
        ESTADO_ACTIVA,
        ESTADO_PAUSADA,
        ESTADO_FINALIZADA,
    )

    def __init__(
        self,
        id_programacion_ahorro,
        monto_periodico,
        fecha_cobro,
        frecuencia,
        fecha_inicio,
        fecha_fin,
        estado
    ):
        self.id_programacion_ahorro = id_programacion_ahorro
        self.monto_periodico = monto_periodico
        self.fecha_cobro = fecha_cobro
        self.frecuencia = frecuencia
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.estado = estado

    @classmethod
    def es_frecuencia_valida(cls, frecuencia):
        return frecuencia in cls.PERIODOS_VALIDOS

    @classmethod
    def es_estado_valido(cls, estado):
        return estado in cls.ESTADOS_VALIDOS

    @classmethod
    def rango_fechas_valido(cls, fecha_inicio, fecha_fin):
        if fecha_fin is None or fecha_inicio is None:
            return True
        return fecha_fin >= fecha_inicio