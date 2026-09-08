from ._servicios import (
    generar_codigo_seis_digitos,
    hash_codigo,
    expiracion_codigo,
)

from ...domain.entity.solicitud_control_parental import (
    SolicitudControlParental,
)

from app.shared.exceptions.control_parental_exception import (
    CorreoPadreNoCoincide,
)


class SolicitarDesvinculacionUseCase:
    def __init__(self, repository, email_service):
        self.repository = repository
        self.email_service = email_service

    def execute(self, id_hijo, correo_padre):
        padre = self.repository.buscar_usuario_por_correo(
            correo_padre
        )

        if not padre:
            raise CorreoPadreNoCoincide()

        vinculacion = (
            self.repository.buscar_vinculacion_activa(
                padre.id_usuario,
                id_hijo,
            )
        )

        if not vinculacion:
            raise CorreoPadreNoCoincide()

        codigo = generar_codigo_seis_digitos()

        self.repository.cancelar_solicitudes_pendientes(
            id_hijo,
            padre.id_usuario,
            SolicitudControlParental.OPERACION_DESVINCULAR,
        )

        solicitud = SolicitudControlParental(
            id_solicitud=None,
            id_usuario_solicitante=id_hijo,
            id_usuario_destino=padre.id_usuario,
            tipo_operacion=(
                SolicitudControlParental.OPERACION_DESVINCULAR
            ),
            token_hash=hash_codigo(codigo),
            fecha_expiracion=expiracion_codigo(),
            correo_confirmacion=padre.correo,
            nombre_confirmacion=None,
            id_control=vinculacion.id_control,
        )

        solicitud = self.repository.crear_solicitud(
            solicitud
        )

        enviado = self.email_service.send_parental_code(
            padre.correo,
            codigo,
            "desvinculación parental",
        )

        if not enviado:
            solicitud.cancelar()
            self.repository.actualizar_solicitud(solicitud)
            raise RuntimeError(
                "No se pudo enviar el código al correo del padre"
            )

        return solicitud
