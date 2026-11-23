import logging

from app.modules.admin.domain.interface.registro_accion_admin_repository import (
    RegistroAccionAdminRepository,
)
from app.modules.usuario.domain.interface.usuario_repository import UsuarioRepository
from app.shared.constants.acciones import ACCION_MODIFICAR_USUARIO
from app.shared.exceptions.auth_errors import EmailAlreadyExistsException
from app.shared.exceptions.common import UsuarioNotFoundException


logger = logging.getLogger(__name__)


class ActualizarUsuarioUseCase:

    def __init__(
        self,
        repository: UsuarioRepository,
        registro_repository: RegistroAccionAdminRepository,
    ):
        self.repository = repository
        self.registro_repository = registro_repository

    def execute(self, id_usuario, usuario_data, id_admin):

        if not self.repository.get_by_id(id_usuario):
            raise UsuarioNotFoundException()

        datos = self._preparar_datos(id_usuario, usuario_data)

        try:
            usuario = self.repository.update(id_usuario, datos)
        except Exception as e:
            logger.error(f"Error al actualizar usuario {id_usuario}: {e}")
            raise

        if not usuario:
            raise UsuarioNotFoundException()

        self._registrar_auditoria(id_usuario, datos, id_admin)

        return usuario

    def _preparar_datos(self, id_usuario, usuario_data):
        """Descarta los campos no enviados o nulos y valida el correo."""
        datos = {
            clave: valor
            for clave, valor in (usuario_data or {}).items()
            if valor is not None
        }

        correo = datos.get("correo")

        if correo is not None:
            datos["correo"] = correo.strip()

            if self.repository.exists_by_email(
                datos["correo"],
                excluir_id_usuario=id_usuario,
            ):
                raise EmailAlreadyExistsException()

        return datos

    def _registrar_auditoria(self, id_usuario, datos, id_admin):
        campos = ", ".join(sorted(datos))

        self.registro_repository.registrar(
            id_admin=id_admin,
            accion=ACCION_MODIFICAR_USUARIO,
            id_usuario_afectado=id_usuario,
            detalle=f"Campos modificados: {campos}" if campos else "Sin cambios",
        )
