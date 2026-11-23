from datetime import datetime, timedelta, timezone

from app.core.constants import MAX_INTENTOS, MINUTOS_BLOQUEO


class IntentoAutenticacion:

    def __init__(self, intentos_fallidos: int, bloqueado_hasta: datetime = None):
        self.intentos_fallidos = intentos_fallidos
        self.bloqueado_hasta = bloqueado_hasta

    def registrar_intento_fallido(self):
        if self.bloqueado_hasta is not None and not self.esta_bloqueado():
            self.intentos_fallidos = 0
            self.bloqueado_hasta = None

        self.intentos_fallidos += 1

        if self.debe_bloquearse():
            self.bloqueado_hasta = (
                datetime.now() + timedelta(minutes=MINUTOS_BLOQUEO)
            )

    def debe_bloquearse(self) -> bool:
        return self.intentos_fallidos >= MAX_INTENTOS

    def esta_bloqueado(self) -> bool:
        if not self.bloqueado_hasta:
            return False
        
        ahora = datetime.now(self.bloqueado_hasta.tzinfo)
        return self.bloqueado_hasta > ahora
