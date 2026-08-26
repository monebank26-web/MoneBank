import logging

from app.modules.usuario.domain.interface.usuario_repository import UsuarioRepository
from app.shared.exceptions.business_exceptions import UsuarioNotFoundException

logger = logging.getLogger(__name__)


class ActualizarUsuarioUseCase:

    def __init__(self, repository: UsuarioRepository):
        self.repository = repository

    def execute(
        self,
        id_usuario,
        usuario_data
    ):
        try:
            usuario = self.repository.update(
                id_usuario,
                usuario_data
            )
        except Exception as e:
            logger.error(f"Error al actualizar usuario {id_usuario}: {e}")
            raise

        if not usuario:
            raise UsuarioNotFoundException()

        return usuario
