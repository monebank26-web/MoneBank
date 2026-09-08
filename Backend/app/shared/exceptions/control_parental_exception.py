class ControlParentalException(Exception):
    status_code = 400
    description = "Error en control parental"
    def __init__(self, message=None):
        self.message = message or self.description
        super().__init__(self.message)

class UsuarioParentalNoEncontrado(ControlParentalException):
    status_code = 404
    description = "No se encontró el usuario indicado"

class VinculacionNoEncontrada(ControlParentalException):
    status_code = 404
    description = "No existe una vinculación parental activa"

class VinculacionDuplicada(ControlParentalException):
    status_code = 409
    description = "Las cuentas ya están vinculadas"

class SolicitudPendienteExiste(ControlParentalException):
    status_code = 409
    description = "Ya existe una solicitud pendiente para estas cuentas"

class CodigoInvalido(ControlParentalException):
    status_code = 400
    description = "El código es inválido o expiró"

class CodigoIntentosAgotados(ControlParentalException):
    status_code = 429
    description = "Se agotaron los intentos para este código"

class AutoVinculacionNoPermitida(ControlParentalException):
    status_code = 400
    description = "No puedes vincular una cuenta consigo misma"

class CorreoPadreNoCoincide(ControlParentalException):
    status_code = 400
    description = "El correo no corresponde al padre vinculado"