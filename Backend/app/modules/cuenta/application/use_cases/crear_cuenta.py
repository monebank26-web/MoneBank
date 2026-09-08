from app.modules.cuenta.domain.entity.cuenta import Cuenta
from app.modules.cuenta.domain.interface.cuenta_repository import CuentaRepository
from app.shared.exceptions.business_exceptions import EstadoInvalido


class CrearCuenta:

    def __init__(self, repository: CuentaRepository):
        self.repository = repository

    def execute(self, cuenta_data):
        cuenta = Cuenta(
            id_cuenta=None,
            saldo=cuenta_data.get("saldo") or 0,
            estado=cuenta_data["estado"],
            id_usuario=cuenta_data["id_usuario"],
        )

        if not Cuenta.es_estado_valido(cuenta.estado):
            raise EstadoInvalido()

        return self.repository.create(cuenta_data)