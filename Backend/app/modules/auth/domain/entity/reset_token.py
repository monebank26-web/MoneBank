from datetime import datetime, timezone


class ResetToken:

    def __init__(self, id=None, usuario_id=None, token_hash=None,
                 fecha_creacion=None, fecha_expiracion=None, usado=False):
        self.id = id
        self.usuario_id = usuario_id
        self.token_hash = token_hash
        self.fecha_creacion = fecha_creacion
        self.fecha_expiracion = fecha_expiracion
        self.usado = usado

    def esta_expirado(self) -> bool:
        exp = self.fecha_expiracion
        if exp.tzinfo is None:
            exp = exp.replace(tzinfo=timezone.utc)
        return exp < datetime.now(timezone.utc)

    def fue_utilizado(self) -> bool:
        return self.usado is True

    def es_valido(self) -> bool:
        return not self.esta_expirado() and not self.fue_utilizado()
