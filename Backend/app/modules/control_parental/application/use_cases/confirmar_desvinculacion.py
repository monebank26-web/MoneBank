from ._servicios import hash_codigo
from ...domain.entity.solicitud_control_parental import (
    SolicitudControlParental,
)
from app.shared.exceptions.control_parental_exception import (
    CodigoInvalido,
    VinculacionNoEncontrada,
)


class ConfirmarDesvinculacionUseCase:
    def __init__(self, repository):
        self.repository = repository

    def execute(self, id_hijo, codigo):
        solicitud = self.repository.buscar_solicitud_vigente(
            hash_codigo(codigo),
            SolicitudControlParental.OPERACION_DESVINCULAR,
        )

        if not solicitud:
            raise CodigoInvalido()


        if solicitud.id_usuario_solicitante != id_hijo:
            raise CodigoInvalido()

        vinculacion = (
            self.repository.buscar_vinculacion_activa(
                solicitud.id_usuario_destino,
                solicitud.id_usuario_solicitante,
            )
        )

        if not vinculacion:
            raise VinculacionNoEncontrada()

        solicitud.confirmar()
        self.repository.actualizar_solicitud(solicitud)

        vinculacion.desvincular()

        return self.repository.actualizar_vinculacion(
            vinculacion
        )
