from app.modules.cuenta.domain.interface.cuenta_repository import CuentaRepository
from app.shared.exceptions.transaccion_errors import (
    CuentaNoEncontrada,
    CuentaNoPerteneceAlUsuario,
)


class ObtenerCuentaPorIdUseCase:

    def __init__(self, repository: CuentaRepository):
        self.repository = repository

    def execute(self, id_cuenta, id_usuario, es_admin):
        cuenta = self.repository.get_cuenta_por_id(id_cuenta)

        if not cuenta:
            raise CuentaNoEncontrada()

        if not es_admin and cuenta.id_usuario != id_usuario:
            raise CuentaNoPerteneceAlUsuario()

        return cuenta
