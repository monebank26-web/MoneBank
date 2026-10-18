from app.modules.cuenta.domain.entity.cuenta import Cuenta
from app.modules.cuenta.domain.interface.cuenta_repository import CuentaRepository
from app.shared.exceptions.cuenta_errors import EstadoCuentaInvalido
from app.shared.exceptions.common import (
    CuentaNoEncontrada,
    CuentaNoPerteneceAlUsuario,
)


class ActualizarCuentaUseCase:

    def __init__(self, repository: CuentaRepository):
        self.repository = repository

    def execute(self, id_cuenta, cuenta_data, id_usuario, es_admin):
        cuenta = self.repository.get_cuenta_por_id(id_cuenta)

        if not cuenta:
            raise CuentaNoEncontrada()

        if not es_admin and cuenta.id_usuario != id_usuario:
            raise CuentaNoPerteneceAlUsuario()

        estado = cuenta_data.get("estado")
        if estado is not None and not Cuenta.es_estado_valido(estado):
            raise EstadoCuentaInvalido()

        return self.repository.update(id_cuenta, cuenta_data)
