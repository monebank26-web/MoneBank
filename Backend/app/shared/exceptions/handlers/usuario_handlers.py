from fastapi import FastAPI

from app.shared.exceptions.auth_errors import EmailAlreadyExistsException
from app.shared.exceptions.handlers._helpers import registrar_error_business
from app.shared.exceptions.usuario_errors import (
    CuentaYaBloqueadaException,
    MotivoBloqueoRequeridoException,
    UsuarioNotFoundException,
)


def register_usuario_exception_handlers(app: FastAPI):
    registrar_error_business(app, EmailAlreadyExistsException, 409)
    registrar_error_business(app, UsuarioNotFoundException, 404)
    registrar_error_business(app, CuentaYaBloqueadaException, 409)
    registrar_error_business(app, MotivoBloqueoRequeridoException, 422)