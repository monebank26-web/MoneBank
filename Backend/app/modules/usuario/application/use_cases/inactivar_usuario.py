from datetime import datetime

from app.core.security.roles import ROL_ADMIN
from app.modules.admin.domain.interface.registro_accion_admin_repository import (
    RegistroAccionAdminRepository,
)
from app.modules.usuario.domain.interface.usuario_repository import UsuarioRepository
from app.shared.constants.acciones import ACCION_DESACTIVAR_USUARIO
from app.shared.constants.estados import ESTADO_INACTIVO, normalizar_estado
from app.shared.exceptions.common import UsuarioNotFoundException
from app.shared.exceptions.usuario_errors import (
    NoPuedeBloquearseException,
    UltimoAdministradorException,
)


class InactivarUsuario:

    def __init__(self, repository: UsuarioRepository, registro_repository: RegistroAccionAdminRepository = None):
        self.repository = repository
        self.registro_repository = registro_repository

    def execute(self, id_usuario, id_admin=None):

        if id_admin is not None and id_admin == id_usuario:
            raise NoPuedeBloquearseException()

        usuario = self.repository.get_by_id(id_usuario)

        if not usuario:
            raise UsuarioNotFoundException()

        if usuario.id_rol == ROL_ADMIN:
            admins_activos = self.repository.contar_admins_activos(excluir_id_usuario=id_usuario)
            if admins_activos == 0:
                raise UltimoAdministradorException()

        usuario_actualizado = self.repository.update(id_usuario, {
            "estado": ESTADO_INACTIVO,
        })

        if self.registro_repository and id_admin is not None:
            self.registro_repository.registrar(
                id_admin=id_admin,
                accion=ACCION_DESACTIVAR_USUARIO,
                id_usuario_afectado=id_usuario,
                detalle="Usuario desactivado",
            )

        return usuario_actualizado
