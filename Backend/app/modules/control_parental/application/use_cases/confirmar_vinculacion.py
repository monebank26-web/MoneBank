from ._servicios import hash_codigo
from ...domain.entity.control_parental import ControlParental
from ...domain.entity.solicitud_control_parental import SolicitudControlParental
from app.shared.exceptions.control_parental_exception import CodigoInvalido, VinculacionDuplicada

class ConfirmarVinculacionUseCase:
    def __init__(self, repository): self.repository = repository
    def execute(self, id_hijo, codigo):
        solicitud = self.repository.buscar_solicitud_vigente(hash_codigo(codigo), SolicitudControlParental.OPERACION_VINCULAR)
        if not solicitud or solicitud.id_usuario_destino != id_hijo:
            raise CodigoInvalido()
        if self.repository.buscar_vinculacion_activa(solicitud.id_usuario_solicitante, id_hijo):
            solicitud.cancelar(); self.repository.actualizar_solicitud(solicitud); raise VinculacionDuplicada()
        solicitud.confirmar(); self.repository.actualizar_solicitud(solicitud)
        vinculacion = ControlParental.crear(solicitud.id_usuario_solicitante, id_hijo)
        return self.repository.guardar_vinculacion(vinculacion)
