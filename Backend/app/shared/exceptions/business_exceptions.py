class InvalidCredentialsException(Exception):
    def __init__(self, message="Credenciales incorrectas"):
        self.message = message
        super().__init__(self.message)


class AccountLockedException(Exception):
    def __init__(self, message="Cuenta bloqueada temporalmente por múltiples intentos fallidos"):
        self.message = message
        super().__init__(self.message)