from app.modules.transaccion.domain.interface.trans_repository import (
    TransaccionRepository
)


class ObtenerCategoriasUseCase:

    def __init__(self, repository: TransaccionRepository):
        self.repository = repository

    def execute(self):
        return self.repository.find_categorias()
