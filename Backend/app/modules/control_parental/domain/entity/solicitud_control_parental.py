from datetime import datetime, timezone
from app.shared.exceptions.control_parental_exception import CodigoIntentosAgotados

class SolicitudControlParental:
    OPERACION_VINCULAR = "VINCULAR"
    OPERACION_DESVINCULAR = "DESVINCULAR"
    ESTADO_PENDIENTE = "PENDIENTE"
    ESTADO_CONFIRMADA = "CONFIRMADA"
    ESTADO_CANCELADA = "CANCELADA"
    MAX_INTENTOS = 5

    def __init__(self, id_solicitud, id_usuario_solicitante, id_usuario_destino,
                 tipo_operacion, token_hash, fecha_expiracion,
                 correo_confirmacion, nombre_confirmacion=None, id_control=None,
                 intentos_fallidos=0, usado=False, estado=ESTADO_PENDIENTE):
        self.id_solicitud = id_solicitud
        self.id_usuario_solicitante = id_usuario_solicitante
        self.id_usuario_destino = id_usuario_destino
        self.tipo_operacion = tipo_operacion
        self.token_hash = token_hash
        self.fecha_expiracion = fecha_expiracion
        self.correo_confirmacion = correo_confirmacion
        self.nombre_confirmacion = nombre_confirmacion
        self.id_control = id_control
        self.intentos_fallidos = intentos_fallidos
        self.usado = usado
        self.estado = estado

    def esta_vigente(self, ahora=None):
        ahora = ahora or datetime.now(timezone.utc)
        return (self.estado == self.ESTADO_PENDIENTE and not self.usado
                and self.fecha_expiracion > ahora
                and self.intentos_fallidos < self.MAX_INTENTOS)

    def registrar_intento_fallido(self):
        self.intentos_fallidos += 1
        if self.intentos_fallidos >= self.MAX_INTENTOS:
            raise CodigoIntentosAgotados()

    def confirmar(self):
        if not self.esta_vigente():
            raise ValueError("La solicitud no está vigente")
        self.usado = True
        self.estado = self.ESTADO_CONFIRMADA
        return self

    def cancelar(self):
        self.usado = True
        self.estado = self.ESTADO_CANCELADA
        return self
