from app.shared.exceptions.ahorro_errors import AhorroNoEncontrado
from app.shared.exceptions.transaccion_errors import CuentaNoEncontrada


class EliminarAhorroUseCase:

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

        return self.repository.delete(id_ahorro)
