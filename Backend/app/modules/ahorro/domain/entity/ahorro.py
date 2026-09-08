from datetime import date, timedelta


class Ahorro:

    TIPO_META = "META"
    TIPO_LIMITE = "LIMITE"

    PERIODO_DIARIO = "DIARIO"
    PERIODO_SEMANAL = "SEMANAL"
    PERIODO_MENSUAL = "MENSUAL"

    ESTADO_ACTIVO = "ACTIVO"
    ESTADO_PAUSADO = "PAUSADO"
    ESTADO_FINALIZADO = "FINALIZADO"

    UMBRAL_ALERTA = 80

    def __init__(
        self,
        id_ahorro,
        nombre,
        monto_objetivo,
        saldo_actual,
        estado,
        fecha_objetivo=None,
        periodo=None,
    ):
        self.id_ahorro = id_ahorro
        self.nombre = nombre
        self.monto_objetivo = monto_objetivo
        self.saldo_actual = saldo_actual
        self.estado = estado
        self.fecha_objetivo = fecha_objetivo
        self.periodo = periodo

    def es_meta(self, nombre_tipo):
        return nombre_tipo == self.TIPO_META

    def es_limite(self, nombre_tipo):
        return nombre_tipo == self.TIPO_LIMITE

    def calcular_porcentaje_avance(self):
        if not self.monto_objetivo:
            return 0
        return (self.saldo_actual / self.monto_objetivo) * 100

    def calcular_dinero_faltante(self):
        if not self.monto_objetivo:
            return 0
        return max(self.monto_objetivo - self.saldo_actual, 0)

    def esta_en_alerta(self, porcentaje_usado):
        return porcentaje_usado >= self.UMBRAL_ALERTA

    def es_fecha_objetivo_valida(self, fecha_actual=None):
        if self.fecha_objetivo is None:
            return False
        fecha_actual = fecha_actual or date.today()
        return self.fecha_objetivo >= fecha_actual

    @classmethod
    def es_periodo_valido(cls, periodo):
        return periodo in (
            cls.PERIODO_DIARIO,
            cls.PERIODO_SEMANAL,
            cls.PERIODO_MENSUAL,
        )

    @classmethod
    def calcular_rango_periodo(cls, periodo, fecha_actual=None):
        if not cls.es_periodo_valido(periodo):
            return None

        fecha_actual = fecha_actual or date.today()

        if periodo == cls.PERIODO_DIARIO:
            return fecha_actual, fecha_actual

        if periodo == cls.PERIODO_SEMANAL:
            inicio = fecha_actual - timedelta(days=fecha_actual.weekday())
            return inicio, fecha_actual

        return fecha_actual.replace(day=1), fecha_actual
