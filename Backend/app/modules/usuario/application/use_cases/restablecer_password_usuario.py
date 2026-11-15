from datetime import datetime, timedelta, timezone

from app.core.constants import MINUTOS_TOKEN_RECUPERACION
from app.core.security.reset_token import TokenGenerator
from app.modules.admin.domain.interface.registro_accion_admin_repository import (
    RegistroAccionAdminRepository,
)
from app.modules.auth.domain.interface.auth_repository import AuthRepository
from app.modules.usuario.domain.interface.usuario_repository import UsuarioRepository
from app.shared.constants.acciones import ACCION_RESTABLECER_PASSWORD
from app.shared.exceptions.common import UsuarioNotFoundException
from app.shared.exceptions.usuario_errors import (
    NoPuedeRestablecerPasswordPropiaException,
)


class RestablecerPasswordUsuario:
    """Genera un enlace de restablecimiento sin cambiar la contraseña actual.

    Invalida los tokens de recuperación anteriores, pero no la contraseña ni
    los intentos fallidos. El envío del correo queda fuera de este caso de uso.
    """

    def __init__(
        self,
        repository: UsuarioRepository,
        auth_repository: AuthRepository,
        registro_repository: RegistroAccionAdminRepository,
    ):
        self.repository = repository
        self.auth_repository = auth_repository
        self.registro_repository = registro_repository

    def execute(self, id_usuario, id_admin):
        if id_admin == id_usuario:
            raise NoPuedeRestablecerPasswordPropiaException()

        usuario = self.repository.get_by_id(id_usuario)

        if not usuario:
            raise UsuarioNotFoundException()

        self.auth_repository.invalidate_user_tokens(id_usuario)

        token_original = TokenGenerator.generate()
        token_hash = TokenGenerator.hash(token_original)

        fecha_expiracion = (
            datetime.now(timezone.utc)
            + timedelta(minutes=MINUTOS_TOKEN_RECUPERACION)
        )

        self.auth_repository.create_recovery_token(
            id_usuario,
            token_hash,
            fecha_expiracion,
        )

        self.registro_repository.registrar(
            id_admin=id_admin,
            accion=ACCION_RESTABLECER_PASSWORD,
            id_usuario_afectado=id_usuario,
            detalle=(
                "Enlace de restablecimiento generado; contraseña vigente"
            ),
        )

        return {
            "id_usuario": id_usuario,
            "correo": usuario.correo,
            "token": token_original,
        }
