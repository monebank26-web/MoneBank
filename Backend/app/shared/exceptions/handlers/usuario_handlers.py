from fastapi import FastAPI

from app.shared.exceptions.handlers._helpers import registrar_error_business
from app.shared.exceptions.usuario_errors import (
    CuentaYaBloqueadaException,
    CuentaYaInactivaException,
    MotivoBloqueoRequeridoException,
    NoPuedeBloquearseException,
    NoPuedeDesactivarseException,
    UltimoAdministradorDesactivacionException,
    UltimoAdministradorException,
)


def register_usuario_exception_handlers(app: FastAPI):
    registrar_error_business(app, CuentaYaBloqueadaException, 409)
    registrar_error_business(app, CuentaYaInactivaException, 409)
    registrar_error_business(app, MotivoBloqueoRequeridoException, 422)
    registrar_error_business(app, NoPuedeBloquearseException, 400)
    registrar_error_business(app, NoPuedeDesactivarseException, 400)
    registrar_error_business(app, UltimoAdministradorException, 409)
    registrar_error_business(
        app,
        UltimoAdministradorDesactivacionException,
        409,
    )