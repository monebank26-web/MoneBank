class ValidationException(Exception):
    status_code = 422
    description = "Datos de entrada inválidos"


class InternalServerException(Exception):
    status_code = 500
    description = "Error interno del servidor"