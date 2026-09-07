from app.shared.exceptions.business_exceptions import CuentaNoEncontrada


class ObtenerMetas:

    def __init__(self, repository, cuenta_repository):
        self.repository = repository
        self.cuenta_repository = cuenta_repository

    def execute(self, id_usuario):

        cuenta = self.cuenta_repository.get_cuenta_por_usuario(id_usuario)

        if not cuenta:
            raise CuentaNoEncontrada()

        return self.repository.get_metas_activas(cuenta.id_cuenta)
