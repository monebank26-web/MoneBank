from app.modules.cuenta.domain.interface.cuenta_repository import CuentaRepository
from app.shared.exceptions.business_exceptions import CuentaNoEncontrada


class ObtenerCuentaPorIdUseCase:

    def __init__(self, repository: CuentaRepository):
        self.repository = repository

    def execute(self, id_cuenta):
        cuenta = self.repository.get_cuenta_por_id(id_cuenta)

        if not cuenta:
            raise CuentaNoEncontrada()

        return cuenta