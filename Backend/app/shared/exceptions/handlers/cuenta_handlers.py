from fastapi import FastAPI

from app.shared.exceptions.cuenta_errors import EstadoCuentaInvalido
from app.shared.exceptions.handlers._helpers import registrar_error_business


def register_cuenta_exception_handlers(app: FastAPI):
    registrar_error_business(app, EstadoCuentaInvalido, 400)
