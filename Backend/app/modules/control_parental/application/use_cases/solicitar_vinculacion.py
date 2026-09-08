from ._servicios import generar_codigo_seis_digitos, hash_codigo, expiracion_codigo
from ...domain.entity.control_parental import ControlParental
from ...domain.entity.solicitud_control_parental import SolicitudControlParental
from app.shared.exceptions.control_parental_exception import UsuarioParentalNoEncontrado, AutoVinculacionNoPermitida, VinculacionDuplicada

class SolicitarVinculacionUseCase:
    def __init__(self, repository, email_service):
        self.repository = repository
        self.email_service = email_service

    def execute(self, id_padre, correo_hijo, nombre_hijo):
        hijo = self.repository.buscar_usuario_por_correo(correo_hijo)
        if not hijo:
            raise UsuarioParentalNoEncontrado()
        if hijo.id_usuario == id_padre:
            raise AutoVinculacionNoPermitida()
        if self.repository.buscar_vinculacion_activa(id_padre, hijo.id_usuario):
            raise VinculacionDuplicada()
        codigo = generar_codigo_seis_digitos()
        self.repository.cancelar_solicitudes_pendientes(id_padre, hijo.id_usuario, SolicitudControlParental.OPERACION_VINCULAR)
        solicitud = SolicitudControlParental(
            id_solicitud=None, id_usuario_solicitante=id_padre,
            id_usuario_destino=hijo.id_usuario,
            tipo_operacion=SolicitudControlParental.OPERACION_VINCULAR,
            token_hash=hash_codigo(codigo), fecha_expiracion=expiracion_codigo(),
            correo_confirmacion=hijo.correo, nombre_confirmacion=nombre_hijo,
        )
        solicitud = self.repository.crear_solicitud(solicitud)
        if not self.email_service.send_parental_code(hijo.correo, codigo, "vinculación parental"):
            solicitud.cancelar(); self.repository.actualizar_solicitud(solicitud)
            raise RuntimeError("No se pudo enviar el código")
        return solicitud