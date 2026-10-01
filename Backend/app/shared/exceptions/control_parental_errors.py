from app.shared.exceptions.base import BusinessError


class ControlParentalException(BusinessError):
    message = "Error en control parental"


class UsuarioParentalNoEncontrado(ControlParentalException):
    message = "No se encontró el usuario indicado"


class VinculacionNoEncontrada(ControlParentalException):
    message = "No existe una vinculación parental activa"


class VinculacionDuplicada(ControlParentalException):
    message = "Las cuentas ya están vinculadas"


class SolicitudPendienteExiste(ControlParentalException):
    message = "Ya existe una solicitud pendiente para estas cuentas"


class CodigoInvalido(ControlParentalException):
    message = "El código es inválido o expiró"


class CodigoIntentosAgotados(ControlParentalException):
    message = "Se agotaron los intentos para este código"


class AutoVinculacionNoPermitida(ControlParentalException):
    message = "No puedes vincular una cuenta consigo misma"


class CorreoPadreNoCoincide(ControlParentalException):
    message = "El correo no corresponde al padre vinculado"