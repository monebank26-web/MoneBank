from calendar import monthrange
from datetime import date, timedelta

from app.shared.exceptions.ahorro_errors import FrecuenciaInvalida


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

    DIAS_POR_FRECUENCIA = {
        PERIODO_DIARIA: 1,
        PERIODO_SEMANAL: 7,
        PERIODO_QUINCENAL: 15,
    }

    MESES_POR_FRECUENCIA = {
        PERIODO_MENSUAL: 1,
        PERIODO_TRIMESTRAL: 3,
        PERIODO_SEMESTRAL: 6,
        PERIODO_ANUAL: 12,
    }

    def __init__(
        self,
        id_programacion_ahorro,
        id_ahorro,
        monto_periodico,
        fecha_cobro,
        frecuencia,
        fecha_inicio,
        fecha_fin,
        estado
    ):
        self.id_programacion_ahorro = id_programacion_ahorro
        self.id_ahorro = id_ahorro
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

    def esta_vencida(self, hoy):
        return self.fecha_cobro is not None and self.fecha_cobro <= hoy

    def calcular_proxima_fecha(self, hoy):
        if not self.es_frecuencia_valida(self.frecuencia):
            raise FrecuenciaInvalida()

        ancla = self.fecha_inicio or self.fecha_cobro
        if ancla is None:
            raise ValueError("La programación no tiene fecha de cobro")

        dias = self.DIAS_POR_FRECUENCIA.get(self.frecuencia)
        if dias is not None:
            periodos = max((hoy - ancla).days // dias, 0)
            while True:
                candidata = ancla + timedelta(days=periodos * dias)
                if candidata > hoy:
                    return candidata
                periodos += 1

        meses_periodo = self.MESES_POR_FRECUENCIA[self.frecuencia]
        diferencia_meses = (
            (hoy.year - ancla.year) * 12 + (hoy.month - ancla.month)
        )
        periodos = max(diferencia_meses // meses_periodo, 0)

        while True:
            candidata = self._sumar_meses(ancla, periodos * meses_periodo)
            if candidata > hoy:
                return candidata
            periodos += 1

    def debe_finalizarse(self, proxima_fecha):
        return self.fecha_fin is not None and proxima_fecha > self.fecha_fin

    def siguiente_estado(self, proxima_fecha):
        if self.debe_finalizarse(proxima_fecha):
            return self.ESTADO_FINALIZADA
        return self.estado

    def _sumar_meses(self, fecha, cantidad):
        anio = fecha.year + (fecha.month - 1 + cantidad) // 12
        mes = (fecha.month - 1 + cantidad) % 12 + 1
        dia_ancla = (self.fecha_inicio or self.fecha_cobro).day
        dia = min(dia_ancla, monthrange(anio, mes)[1])
        return date(anio, mes, dia)
