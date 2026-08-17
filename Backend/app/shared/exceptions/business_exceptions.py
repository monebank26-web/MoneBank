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


class EmailAlreadyExistsException(Exception):
    status_code = 409
    description = "El correo ya está registrado"

    def __init__(self, message: str = None):
        self.message = message or self.description
        super().__init__(self.message)


class EmailNotFoundException(Exception):
    status_code = 404
    description = "El correo no está registrado"

    def __init__(self, message: str = None):
        self.message = message or self.description
        super().__init__(self.message)


class InvalidOrExpiredTokenException(Exception):
    status_code = 410
    description = "El token es inválido o ha expirado"

    def __init__(self, message: str = None):
        self.message = message or self.description
        super().__init__(self.message)