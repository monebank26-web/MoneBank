from app.shared.constants.codigos_error import (
    CODIGO_CUENTA_INACTIVA_NO_BLOQUEABLE,
    CODIGO_CUENTA_YA_BLOQUEADA,
    CODIGO_CUENTA_YA_INACTIVA,
    CODIGO_NO_PUEDE_BLOQUEARSE,
    CODIGO_NO_PUEDE_DESACTIVARSE,
    CODIGO_ULTIMO_ADMINISTRADOR,
)
from app.shared.exceptions.base import BusinessError


class CuentaYaBloqueadaException(BusinessError):
    message = "La cuenta ya se encuentra bloqueada"
    code = CODIGO_CUENTA_YA_BLOQUEADA


class CuentaInactivaNoBloqueableException(BusinessError):
    message = "No se puede bloquear una cuenta inactiva"
    code = CODIGO_CUENTA_INACTIVA_NO_BLOQUEABLE


class CuentaYaInactivaException(BusinessError):
    message = "No se puede desactivar una cuenta ya inactiva"
    code = CODIGO_CUENTA_YA_INACTIVA


class MotivoBloqueoRequeridoException(BusinessError):
    message = "El motivo del bloqueo es obligatorio"


class NoPuedeBloquearseException(BusinessError):
    message = "No puedes bloquear tu propia cuenta"
    code = CODIGO_NO_PUEDE_BLOQUEARSE


class UltimoAdministradorException(BusinessError):
    message = "No se puede bloquear al último administrador activo"
    code = CODIGO_ULTIMO_ADMINISTRADOR


class NoPuedeDesactivarseException(BusinessError):
    message = "No puedes desactivar tu propia cuenta"
    code = CODIGO_NO_PUEDE_DESACTIVARSE


class UltimoAdministradorDesactivacionException(BusinessError):
    message = "No se puede desactivar al último administrador activo"
    code = CODIGO_ULTIMO_ADMINISTRADOR
