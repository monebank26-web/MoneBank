from ._servicios import hash_codigo
from ...domain.entity.control_parental import ControlParental
from ...domain.entity.solicitud_control_parental import SolicitudControlParental
from app.shared.exceptions.control_parental_errors import (
    CodigoInvalido,
    VinculacionDuplicada,
)

class ConfirmarVinculacionUseCase:
    def __init__(self, repository): self.repository = repository
    def execute(self, id_padre, codigo):
        solicitud = self.repository.buscar_solicitud_vigente(hash_codigo(codigo), SolicitudControlParental.OPERACION_VINCULAR)
        if not solicitud or solicitud.id_usuario_solicitante != id_padre:
            raise CodigoInvalido()
        id_hijo = solicitud.id_usuario_destino
        if self.repository.buscar_vinculacion_activa(id_padre, id_hijo):
            solicitud.cancelar(); self.repository.actualizar_solicitud(solicitud); raise VinculacionDuplicada()
        solicitud.confirmar(); self.repository.actualizar_solicitud(solicitud)
        vinculacion = ControlParental.crear(id_padre, id_hijo)
        return self.repository.guardar_vinculacion(vinculacion)
