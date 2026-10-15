from app.shared.exceptions.base import BusinessError


class CuentaNoEncontrada(BusinessError):
    message = "Cuenta no encontrada"


class CuentaNoPerteneceAlUsuario(BusinessError):
    message = "La cuenta no pertenece al usuario autenticado"


class SaldoInsuficiente(BusinessError):
    message = "Saldo insuficiente en la cuenta"


class MontoInvalido(BusinessError):
    message = "El monto debe ser mayor a 0"


class CategoriaInvalida(BusinessError):
    message = "La categoría no existe en el catálogo"


class UsuarioNotFoundException(BusinessError):
    message = "Usuario no encontrado"
