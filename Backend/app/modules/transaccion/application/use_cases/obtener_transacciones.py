from app.modules.transaccion.domain.interface.trans_repository import (
    TransaccionRepository
)
from app.shared.exceptions.transaccion import TransaccionesNoEncontrado


class ObtenerTransaccionesUseCase:

    def __init__(self, repository: TransaccionRepository):
        self.repository = repository

    def execute(self, usuario_id):
        transacciones = self.repository.find_by_usuario(
            usuario_id,
        )

        if not transacciones:
            raise TransaccionesNoEncontrado()

        return transacciones
