from datetime import datetime, timezone

from app.core.constants import MAX_INTENTOS_CODIGO_RECUPERACION


class ResetToken:

    def __init__(self, id=None, usuario_id=None, token_hash=None,
                 fecha_creacion=None, fecha_expiracion=None, usado=False,
                 intentos_fallidos=0):
        self.id = id
        self.usuario_id = usuario_id
        self.token_hash = token_hash
        self.fecha_creacion = fecha_creacion
        self.fecha_expiracion = fecha_expiracion
        self.usado = usado
        self.intentos_fallidos = intentos_fallidos or 0

    def esta_expirado(self) -> bool:
        exp = self.fecha_expiracion
        if exp.tzinfo is None:
            exp = exp.replace(tzinfo=timezone.utc)
        return exp < datetime.now(timezone.utc)

    def fue_utilizado(self) -> bool:
        return self.usado is True

    def esta_agotado(self) -> bool:
        return self.intentos_fallidos >= MAX_INTENTOS_CODIGO_RECUPERACION

    def registrar_intento_fallido(self) -> None:
        self.intentos_fallidos += 1

        if self.esta_agotado():
            self.usado = True

    def es_valido(self) -> bool:
        return (
            not self.esta_expirado()
            and not self.fue_utilizado()
            and not self.esta_agotado()
        )
