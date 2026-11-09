from app.shared.constants.codigos_error import (
    CODIGO_CORREO_RESTABLECIMIENTO_NO_ENVIADO,
    CODIGO_CUENTA_INACTIVA_NO_BLOQUEABLE,
    CODIGO_CUENTA_NO_BLOQUEADA,
    CODIGO_CUENTA_YA_BLOQUEADA,
    CODIGO_CUENTA_YA_INACTIVA,
    CODIGO_NO_PUEDE_BLOQUEARSE,
    CODIGO_NO_PUEDE_DESACTIVARSE,
    CODIGO_NO_PUEDE_RESTABLECER_PASSWORD_PROPIA,
    CODIGO_ULTIMO_ADMINISTRADOR,
)
from app.shared.exceptions.base import BusinessError


class CuentaYaBloqueadaException(BusinessError):
    message = "La cuenta ya se encuentra bloqueada"
    code = CODIGO_CUENTA_YA_BLOQUEADA


class CuentaInactivaNoBloqueableException(BusinessError):
    message = "No se puede bloquear una cuenta inactiva"
    code = CODIGO_CUENTA_INACTIVA_NO_BLOQUEABLE


class CuentaNoBloqueadaException(BusinessError):
    message = "La cuenta no se encuentra bloqueada ni desactivada"
    code = CODIGO_CUENTA_NO_BLOQUEADA


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


class NoPuedeRestablecerPasswordPropiaException(BusinessError):
    message = "No puedes restablecer tu propia contraseña desde este endpoint"
    code = CODIGO_NO_PUEDE_RESTABLECER_PASSWORD_PROPIA


class CorreoRestablecimientoNoEnviadoException(BusinessError):
    message = (
        "La contraseña fue invalidada, pero el correo no pudo enviarse. "
        "Reintenta el restablecimiento."
    )
    code = CODIGO_CORREO_RESTABLECIMIENTO_NO_ENVIADO


class UltimoAdministradorDesactivacionException(BusinessError):
    message = "No se puede desactivar al último administrador activo"
    code = CODIGO_ULTIMO_ADMINISTRADOR
