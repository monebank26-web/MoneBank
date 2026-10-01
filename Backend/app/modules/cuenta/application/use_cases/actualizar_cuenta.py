from app.modules.cuenta.domain.entity.cuenta import Cuenta
from app.modules.cuenta.domain.interface.cuenta_repository import CuentaRepository
from app.shared.exceptions.ahorro_errors import EstadoInvalido
from app.shared.exceptions.transaccion_errors import CuentaNoEncontrada


class ActualizarCuentaUseCase:

    def __init__(self, repository: CuentaRepository):
        self.repository = repository

    def execute(self, id_cuenta, cuenta_data):
        cuenta = self.repository.get_cuenta_por_id(id_cuenta)

        if not cuenta:
            raise CuentaNoEncontrada()

        estado = cuenta_data.get("estado")
        if estado is not None and not Cuenta.es_estado_valido(estado):
            raise EstadoInvalido()

        return self.repository.update(id_cuenta, cuenta_data)