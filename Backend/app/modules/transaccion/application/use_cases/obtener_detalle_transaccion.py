
from app.modules.transaccion.domain.interface.trans_repository import (
    TransaccionRepository
)
from app.shared.exceptions.business_exceptions import TransaccionesNoEncontrado



class ObtenerDetalleUseCase:
    def __init__(self, repository: TransaccionRepository):
        self.repository = repository

    def execute(self, id_usuario: int, id_transaccion: int):
        detalle = self.repository.find_detalle(id_usuario, id_transaccion)
        if detalle is None:
            raise TransaccionesNoEncontrado()
        return detalle