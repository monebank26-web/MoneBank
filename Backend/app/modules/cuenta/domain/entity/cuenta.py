from datetime import date


class Cuenta:

    ESTADO_ACTIVA = "ACTIVA"
    ESTADO_INACTIVA = "INACTIVA"

    def __init__(
        self,
        id_cuenta,
        saldo,
        estado,
        id_usuario,
        fecha_creacion=None,
    ):
        self.id_cuenta = id_cuenta
        self.saldo = saldo
        self.estado = estado
        self.id_usuario = id_usuario
        self.fecha_creacion = fecha_creacion or date.today()

    @classmethod
    def es_estado_valido(cls, estado):
        return estado in (
            cls.ESTADO_ACTIVA,
            cls.ESTADO_INACTIVA,
        )

    def esta_activa(self):
        return self.estado == self.ESTADO_ACTIVA

    def tiene_saldo_suficiente(self, monto):
        return self.saldo >= monto

    def descontar(self, monto):
        if not self.tiene_saldo_suficiente(monto):
            return False
        self.saldo -= monto
        return True

    def acreditar(self, monto):
        self.saldo += monto