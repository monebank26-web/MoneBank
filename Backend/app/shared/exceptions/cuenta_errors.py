from app.shared.exceptions.base import BusinessError


class EstadoCuentaInvalido(BusinessError):
    message = "El estado debe ser ACTIVA o INACTIVA"
