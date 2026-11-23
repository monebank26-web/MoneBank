from typing import Callable, Optional

from app.modules.admin.domain.interface.registro_accion_admin_repository import (
    RegistroAccionAdminRepository,
)
from app.modules.usuario.domain.interface.usuario_repository import UsuarioRepository
from app.shared.constants.acciones import ACCION_RESTABLECER_PASSWORD
from app.shared.exceptions.common import UsuarioNotFoundException
from app.shared.exceptions.usuario_errors import (
    NoPuedeRestablecerPasswordPropiaException,
    SolicitudCodigoRecienteException,
)


class RestablecerPasswordUsuario:
    """Genera un código de restablecimiento sin cambiar la contraseña actual.

    Invalida los códigos de recuperación anteriores, pero no la contraseña ni
    los intentos fallidos. El envío del correo queda fuera de este caso de uso.
    """

    def __init__(
        self,
        repository: UsuarioRepository,
        registro_repository: RegistroAccionAdminRepository,
        generar_codigo: Callable[[int], Optional[str]],
    ):
        self.repository = repository
        self.registro_repository = registro_repository
        self.generar_codigo = generar_codigo

    def execute(self, id_usuario, id_admin):
        if id_admin == id_usuario:
            raise NoPuedeRestablecerPasswordPropiaException()

        usuario = self.repository.get_by_id(id_usuario)

        if not usuario:
            raise UsuarioNotFoundException()

        codigo = self.generar_codigo(id_usuario)

        if codigo is None:
            raise SolicitudCodigoRecienteException()

        self.registro_repository.registrar(
            id_admin=id_admin,
            accion=ACCION_RESTABLECER_PASSWORD,
            id_usuario_afectado=id_usuario,
            detalle=(
                "Código de restablecimiento generado; contraseña vigente"
            ),
        )

        return {
            "id_usuario": id_usuario,
            "correo": usuario.correo,
            "codigo": codigo,
        }
