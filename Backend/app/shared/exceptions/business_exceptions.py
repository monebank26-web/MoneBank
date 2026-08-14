class InvalidCredentialsException(Exception):
    status_code = 401
    description = "Credenciales incorrectas"

    def __init__(self, message: str = None):
        self.message = message or self.description
        super().__init__(self.message)


class AccountLockedException(Exception):
    status_code = 423
    description = "Cuenta bloqueada temporalmente por múltiples intentos fallidos"

    def __init__(self, message: str = None):
        self.message = message or self.description
        super().__init__(self.message)