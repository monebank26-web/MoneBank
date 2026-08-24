from app.shared.exceptions.business_exceptions import CuentaNoEncontrada


class ObtenerAhorrosUseCase:

    def __init__(self, repository):
        self.repository = repository

    def execute(self, id_usuario):

        cuenta = self.repository.get_cuenta_por_usuario(id_usuario)

        if not cuenta:
            raise CuentaNoEncontrada()

        return self.repository.get_by_cuenta(cuenta.id_cuenta)
