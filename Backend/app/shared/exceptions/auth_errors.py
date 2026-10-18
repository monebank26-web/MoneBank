from app.shared.exceptions.base import BusinessError


class InvalidCredentialsException(BusinessError):
    message = "Credenciales incorrectas"


class AccountLockedException(BusinessError):
    message = "Cuenta bloqueada temporalmente por múltiples intentos fallidos"


class EmailAlreadyExistsException(BusinessError):
    message = "El correo ya está registrado"


class EmailNotFoundException(BusinessError):
    message = "El correo no está registrado"


class InvalidOrExpiredTokenException(BusinessError):
    message = "El token es inválido o ha expirado"