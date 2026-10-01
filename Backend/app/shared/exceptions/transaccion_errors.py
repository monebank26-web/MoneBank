from app.shared.exceptions.base import BusinessError


class TransaccionesNoEncontrado(BusinessError):
    message = "No se encontraron transacciones"


class TransaccionNoEditable(BusinessError):
    message = "Esta transacción no se puede editar"


class MontoInvalido(BusinessError):
    message = "El monto del gasto debe ser mayor a 0"


class FechaInvalida(BusinessError):
    message = "La fecha del gasto no es válida"


class CategoriaInvalida(BusinessError):
    message = "La categoría no existe en el catálogo"


class TipoTransaccionNoValido(BusinessError):
    message = "El tipo de transacción no existe en el catálogo"


class AhorroAsociadoNoValido(BusinessError):
    message = "El ahorro asociado no existe o no pertenece a la cuenta"


class CuentaNoEncontrada(BusinessError):
    message = "Cuenta no encontrada"


class CuentaNoPerteneceAlUsuario(BusinessError):
    message = "La cuenta no pertenece al usuario autenticado"


class SaldoInsuficiente(BusinessError):
    message = "Saldo insuficiente en la cuenta"