from app.shared.exceptions.base import BusinessError


class CuentaYaBloqueadaException(BusinessError):
    message = "La cuenta ya se encuentra bloqueada"


class MotivoBloqueoRequeridoException(BusinessError):
    message = "El motivo del bloqueo es obligatorio"
