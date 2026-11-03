from datetime import datetime

from app.modules.admin.domain.interface.registro_accion_admin_repository import (
    RegistroAccionAdminRepository,
)
from app.modules.usuario.domain.interface.usuario_repository import UsuarioRepository
from app.shared.constants.acciones import ACCION_DESBLOQUEAR_USUARIO
from app.shared.constants.estados import (
    ESTADO_ACTIVO,
    ESTADO_BLOQUEADO,
    ESTADO_INACTIVO,
    normalizar_estado,
)
from app.shared.exceptions.common import UsuarioNotFoundException
from app.shared.exceptions.usuario_errors import CuentaNoBloqueadaException


class DesbloquearUsuario:

    def __init__(
        self,
        repository: UsuarioRepository,
        registro_repository: RegistroAccionAdminRepository,
    ):
        self.repository = repository
        self.registro_repository = registro_repository

    def execute(self, id_usuario, id_admin):

        usuario = self.repository.get_by_id(id_usuario)

        if not usuario:
            raise UsuarioNotFoundException()

        estado_anterior = normalizar_estado(usuario.estado)
        bloqueo_temporal_vigente = (
            usuario.bloqueado_hasta is not None
            and usuario.bloqueado_hasta > datetime.now(usuario.bloqueado_hasta.tzinfo)
        )

        if not (
            estado_anterior in (ESTADO_BLOQUEADO, ESTADO_INACTIVO)
            or (estado_anterior == ESTADO_ACTIVO and bloqueo_temporal_vigente)
        ):
            raise CuentaNoBloqueadaException()

        fecha_desbloqueo = datetime.utcnow()

        usuario_actualizado = self.repository.update(id_usuario, {
            "estado": ESTADO_ACTIVO,
            "motivo_bloqueo": None,
            "fecha_bloqueo": None,
            "fecha_desbloqueo": fecha_desbloqueo,
            "intentos_fallidos": 0,
            "bloqueado_hasta": None,
        })

        motivo_anterior = self._motivo_anterior(
            usuario,
            estado_anterior,
            bloqueo_temporal_vigente,
        )

        self.registro_repository.registrar(
            id_admin=id_admin,
            accion=ACCION_DESBLOQUEAR_USUARIO,
            id_usuario_afectado=id_usuario,
            detalle=(
                f"Usuario desbloqueado desde estado {estado_anterior}. "
                f"Motivo anterior: {motivo_anterior}"
            ),
        )

        return usuario_actualizado

    def _motivo_anterior(self, usuario, estado_anterior, bloqueo_temporal_vigente):
        if usuario.motivo_bloqueo:
            return usuario.motivo_bloqueo

        if estado_anterior == ESTADO_ACTIVO and bloqueo_temporal_vigente:
            return "bloqueo temporal por intentos fallidos"

        return "Sin motivo"
