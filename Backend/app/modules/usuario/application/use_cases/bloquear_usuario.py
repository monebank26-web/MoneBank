from datetime import datetime

from app.modules.usuario.domain.interface.usuario_repository import UsuarioRepository
from app.shared.exceptions.business_exceptions import (
    UsuarioNotFoundException,
    CuentaYaBloqueadaException,
    MotivoBloqueoRequeridoException,
)


class BloquearUsuario:

    def __init__(self, repository: UsuarioRepository):
        self.repository = repository

    def execute(self, id_usuario, motivo):

        if not motivo or not motivo.strip():
            raise MotivoBloqueoRequeridoException()

        usuario = self.repository.get_by_id(id_usuario)

        if not usuario:
            raise UsuarioNotFoundException()

        if usuario.estado == "Bloqueado":
            raise CuentaYaBloqueadaException()

        usuario_actualizado = self.repository.update(id_usuario, {
            "estado": "Bloqueado",
            "motivo_bloqueo": motivo.strip(),
            "fecha_bloqueo": datetime.utcnow(),
        })

        return usuario_actualizado
