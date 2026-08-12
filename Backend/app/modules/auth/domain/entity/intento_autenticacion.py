from datetime import datetime, timezone

MAX_INTENTOS = 3


class IntentoAutenticacion:

    def __init__(self, intentos_fallidos: int, bloqueado_hasta: datetime = None):
        self.intentos_fallidos = intentos_fallidos
        self.bloqueado_hasta = bloqueado_hasta

    def debe_bloquearse(self) -> bool:
        return self.intentos_fallidos >= MAX_INTENTOS

    def esta_bloqueado(self) -> bool:
        if not self.bloqueado_hasta:
            return False
        return self.bloqueado_hasta > datetime.now(timezone.utc)