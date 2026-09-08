from datetime import datetime, timezone
from app.shared.exceptions.control_parental_exception import (
    AutoVinculacionNoPermitida, VinculacionDuplicada,
)

class ControlParental:
    ESTADO_ACTIVO = "ACTIVO"
    ESTADO_FINALIZADO = "FINALIZADO"

    ESTADOS_VALIDOS = (ESTADO_ACTIVO, ESTADO_FINALIZADO)

    def __init__(self, id_control, id_usuario_parental, id_usuario_dependiente,
                 permiso_monitoreo=True, estado=ESTADO_ACTIVO,
                 fecha_inicio=None, fecha_fin=None):
        self.id_control = id_control
        self.id_usuario_parental = id_usuario_parental
        self.id_usuario_dependiente = id_usuario_dependiente
        self.permiso_monitoreo = permiso_monitoreo
        self.estado = estado
        self.fecha_inicio = fecha_inicio or datetime.now(timezone.utc)
        self.fecha_fin = fecha_fin
        self.validar_invariantes()

    def validar_invariantes(self):
        if self.id_usuario_parental == self.id_usuario_dependiente:
            raise AutoVinculacionNoPermitida()
        if self.estado not in self.ESTADOS_VALIDOS:
            raise ValueError("Estado de control parental inválido")
        if self.estado == self.ESTADO_ACTIVO and self.fecha_fin is not None:
            raise ValueError("Una relación activa no puede tener fecha de fin")

    @classmethod
    def crear(cls, id_usuario_parental, id_usuario_dependiente):
        return cls(None, id_usuario_parental, id_usuario_dependiente, True, cls.ESTADO_ACTIVO)

    def desvincular(self, fecha_fin=None):
        if self.estado != self.ESTADO_ACTIVO:
            raise VinculacionDuplicada("La vinculación ya está inactiva")
        self.estado = self.ESTADO_FINALIZADO
        self.fecha_fin = fecha_fin or datetime.now(timezone.utc)
        return self
