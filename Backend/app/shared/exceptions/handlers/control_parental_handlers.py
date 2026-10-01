from fastapi import FastAPI

from app.shared.exceptions.control_parental_errors import (
    AutoVinculacionNoPermitida,
    CodigoIntentosAgotados,
    CodigoInvalido,
    CorreoPadreNoCoincide,
    SolicitudPendienteExiste,
    UsuarioParentalNoEncontrado,
    VinculacionDuplicada,
    VinculacionNoEncontrada,
)
from app.shared.exceptions.handlers._helpers import registrar_error_business


def register_control_parental_exception_handlers(app: FastAPI):
    registrar_error_business(app, UsuarioParentalNoEncontrado, 404)
    registrar_error_business(app, VinculacionNoEncontrada, 404)
    registrar_error_business(app, VinculacionDuplicada, 409)
    registrar_error_business(app, SolicitudPendienteExiste, 409)
    registrar_error_business(app, CodigoInvalido, 400)
    registrar_error_business(app, CodigoIntentosAgotados, 429)
    registrar_error_business(app, AutoVinculacionNoPermitida, 400)
    registrar_error_business(app, CorreoPadreNoCoincide, 400)