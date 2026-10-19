from app.shared.constants.codigos_error import (
    CODIGO_CORREO_DUPLICADO,
    CODIGO_CUENTA_BLOQUEADA,
    CODIGO_CUENTA_INACTIVA,
)
from app.shared.exceptions.base import BusinessError


class InvalidCredentialsException(BusinessError):
    message = "Credenciales incorrectas"


class AccountLockedException(BusinessError):
    message = "Cuenta bloqueada temporalmente por múltiples intentos fallidos"


class CuentaBloqueadaException(BusinessError):
    message = "La cuenta está bloqueada por el administrador"
    code = CODIGO_CUENTA_BLOQUEADA


class CuentaInactivaException(BusinessError):
    message = "La cuenta no está activa"
    code = CODIGO_CUENTA_INACTIVA


class EmailAlreadyExistsException(BusinessError):
    message = "El correo ya está registrado"
    code = CODIGO_CORREO_DUPLICADO


class EmailNotFoundException(BusinessError):
    message = "El correo no está registrado"


class InvalidOrExpiredTokenException(BusinessError):
    message = "El token es inválido o ha expirado"