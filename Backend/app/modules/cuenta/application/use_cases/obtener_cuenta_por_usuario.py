from app.modules.cuenta.domain.interface.cuenta_repository import CuentaRepository
from app.shared.exceptions.business_exceptions import CuentaNoEncontrada


class ObtenerCuentaPorUsuarioUseCase:

    def __init__(self, repository: CuentaRepository):
        self.repository = repository

    def execute(self, id_usuario):
        cuenta = self.repository.get_cuenta_por_usuario(id_usuario)

        if not cuenta:
            raise CuentaNoEncontrada()

        return cuenta