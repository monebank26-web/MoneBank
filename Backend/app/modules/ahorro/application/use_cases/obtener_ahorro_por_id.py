from app.shared.exceptions.business_exceptions import (
    AhorroNoEncontrado,
    CuentaNoEncontrada,
)


class ObtenerAhorroPorIdUseCase:

    def __init__(self, repository, cuenta_repository):
        self.repository = repository
        self.cuenta_repository = cuenta_repository

    def execute(self, id_ahorro, id_usuario):

        cuenta = self.cuenta_repository.get_cuenta_por_usuario(id_usuario)

        if not cuenta:
            raise CuentaNoEncontrada()

        ahorro = self.repository.get_by_id(id_ahorro)

        if not ahorro or ahorro.id_cuenta != cuenta.id_cuenta:
            raise AhorroNoEncontrado()

        return ahorro
