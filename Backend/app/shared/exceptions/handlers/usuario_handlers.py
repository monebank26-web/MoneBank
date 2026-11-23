from fastapi import FastAPI

from app.shared.exceptions.handlers._helpers import registrar_error_business
from app.shared.exceptions.usuario_errors import (
    CorreoRestablecimientoNoEnviadoException,
    CuentaInactivaNoBloqueableException,
    CuentaNoBloqueadaException,
    CuentaYaBloqueadaException,
    CuentaYaInactivaException,
    MotivoBloqueoRequeridoException,
    NoPuedeBloquearseException,
    NoPuedeDesactivarseException,
    NoPuedeRestablecerPasswordPropiaException,
    SolicitudCodigoRecienteException,
    UltimoAdministradorDesactivacionException,
    UltimoAdministradorException,
)


def register_usuario_exception_handlers(app: FastAPI):
    registrar_error_business(app, CuentaYaBloqueadaException, 409)
    registrar_error_business(app, CuentaInactivaNoBloqueableException, 409)
    registrar_error_business(app, CuentaNoBloqueadaException, 409)
    registrar_error_business(app, CuentaYaInactivaException, 409)
    registrar_error_business(app, MotivoBloqueoRequeridoException, 422)
    registrar_error_business(app, NoPuedeBloquearseException, 400)
    registrar_error_business(app, NoPuedeDesactivarseException, 400)
    registrar_error_business(
        app,
        NoPuedeRestablecerPasswordPropiaException,
        400,
    )
    registrar_error_business(
        app,
        CorreoRestablecimientoNoEnviadoException,
        502,
    )
    registrar_error_business(app, SolicitudCodigoRecienteException, 429)
    registrar_error_business(app, UltimoAdministradorException, 409)
    registrar_error_business(
        app,
        UltimoAdministradorDesactivacionException,
        409,
    )