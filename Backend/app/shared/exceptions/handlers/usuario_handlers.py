from fastapi import FastAPI

from app.shared.exceptions.handlers._helpers import registrar_error_business
from app.shared.exceptions.usuario_errors import (
    CuentaYaBloqueadaException,
    MotivoBloqueoRequeridoException,
)


def register_usuario_exception_handlers(app: FastAPI):
    registrar_error_business(app, CuentaYaBloqueadaException, 409)
    registrar_error_business(app, MotivoBloqueoRequeridoException, 422)