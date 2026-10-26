from datetime import datetime

from app.core.security.roles import ROL_ADMIN
from app.modules.admin.domain.interface.registro_accion_admin_repository import (
    RegistroAccionAdminRepository,
)
from app.modules.usuario.domain.interface.usuario_repository import UsuarioRepository
from app.shared.constants.acciones import ACCION_BLOQUEAR_USUARIO
from app.shared.constants.estados import (
    ESTADO_BLOQUEADO,
    ESTADO_INACTIVO,
    normalizar_estado,
)
from app.shared.constants.motivo_bloqueo import LONGITUD_MINIMA_MOTIVO_BLOQUEO
from app.shared.exceptions.common import UsuarioNotFoundException
from app.shared.exceptions.usuario_errors import (
    CuentaInactivaNoBloqueableException,
    CuentaYaBloqueadaException,
    MotivoBloqueoRequeridoException,
    NoPuedeBloquearseException,
    UltimoAdministradorException,
)


class BloquearUsuario:

    def __init__(self, repository: UsuarioRepository, registro_repository: RegistroAccionAdminRepository):
        self.repository = repository
        self.registro_repository = registro_repository

    def execute(self, id_usuario, motivo, id_admin):

        motivo_limpio = (motivo or "").strip()

        if len(motivo_limpio) < LONGITUD_MINIMA_MOTIVO_BLOQUEO:
            raise MotivoBloqueoRequeridoException()

        if id_admin == id_usuario:
            raise NoPuedeBloquearseException()

        usuario = self.repository.get_by_id(id_usuario)

        if not usuario:
            raise UsuarioNotFoundException()

        if normalizar_estado(usuario.estado) == ESTADO_BLOQUEADO:
            raise CuentaYaBloqueadaException()

        if normalizar_estado(usuario.estado) == ESTADO_INACTIVO:
            raise CuentaInactivaNoBloqueableException()

        if usuario.id_rol == ROL_ADMIN:
            admins_activos = self.repository.contar_admins_activos(excluir_id_usuario=id_usuario)
            if admins_activos == 0:
                raise UltimoAdministradorException()

        usuario_actualizado = self.repository.update(id_usuario, {
            "estado": ESTADO_BLOQUEADO,
            "motivo_bloqueo": motivo_limpio,
            "fecha_bloqueo": datetime.utcnow(),
        })

        self.registro_repository.registrar(
            id_admin=id_admin,
            accion=ACCION_BLOQUEAR_USUARIO,
            id_usuario_afectado=id_usuario,
            detalle=f"Usuario bloqueado. Motivo: {motivo_limpio}",
        )

        return usuario_actualizado
