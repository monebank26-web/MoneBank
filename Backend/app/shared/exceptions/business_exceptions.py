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


class UsuarioNotFoundException(Exception):
    status_code = 404
    description = "Usuario no encontrado"

    def __init__(self, message: str = None):
        self.message = message or self.description
        super().__init__(self.message)


class TransaccionesNoEncontrado(Exception):
    status_code = 404
    description = "No se encontraron transacciones"

    def __init__(self, message: str = None):
        self.message = message or self.description
        super().__init__(self.message)


class MontoInvalido(Exception):
    status_code = 400
    description = "El monto del gasto debe ser mayor a 0"

    def __init__(self, message: str = None):
        self.message = message or self.description
        super().__init__(self.message)


class FechaInvalida(Exception):
    status_code = 400
    description = "La fecha del gasto no es válida"

    def __init__(self, message: str = None):
        self.message = message or self.description
        super().__init__(self.message)


class CategoriaInvalida(Exception):
    status_code = 422
    description = "La categoría no existe en el catálogo"

    def __init__(self, message: str = None):
        self.message = message or self.description
        super().__init__(self.message)


class TipoTransaccionNoValido(Exception):
    status_code = 422
    description = "El tipo de transacción no existe en el catálogo"

    def __init__(self, message: str = None):
        self.message = message or self.description
        super().__init__(self.message)


class AhorroAsociadoNoValido(Exception):
    status_code = 422
    description = "El ahorro asociado no existe o no pertenece a la cuenta"

    def __init__(self, message: str = None):
        self.message = message or self.description
        super().__init__(self.message)


class CuentaNoEncontrada(Exception):
    status_code = 404
    description = "Cuenta no encontrada"

    def __init__(self, message: str = None):
        self.message = message or self.description
        super().__init__(self.message)


class CuentaNoPerteneceAlUsuario(Exception):
    status_code = 403
    description = "La cuenta no pertenece al usuario autenticado"

    def __init__(self, message: str = None):
        self.message = message or self.description
        super().__init__(self.message)