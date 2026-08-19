from app.modules.cuenta.domain.interface.cuenta_repository import CuentaRepository


class CrearCuenta:

    def __init__(self, repository: CuentaRepository):
        self.repository = repository

    def execute(self, cuenta_data):
        return self.repository.create(cuenta_data)
