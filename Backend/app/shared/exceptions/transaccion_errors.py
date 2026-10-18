from app.shared.exceptions.base import BusinessError


class TransaccionesNoEncontrado(BusinessError):
    message = "No se encontraron transacciones"


class TransaccionNoEditable(BusinessError):
    message = "Esta transacción no se puede editar"


class FechaInvalida(BusinessError):
    message = "La fecha del gasto no es válida"


class TipoTransaccionNoValido(BusinessError):
    message = "El tipo de transacción no existe en el catálogo"


class AhorroAsociadoNoValido(BusinessError):
    message = "El ahorro asociado no existe o no pertenece a la cuenta"
