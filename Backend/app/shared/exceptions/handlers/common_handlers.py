from fastapi import FastAPI

from app.shared.exceptions.common import (
    CategoriaInvalida,
    CuentaNoEncontrada,
    CuentaNoPerteneceAlUsuario,
    MontoInvalido,
    SaldoInsuficiente,
    UsuarioNotFoundException,
)
from app.shared.exceptions.handlers._helpers import registrar_error_business


def register_common_exception_handlers(app: FastAPI):
    registrar_error_business(app, CuentaNoEncontrada, 404)
    registrar_error_business(app, CuentaNoPerteneceAlUsuario, 403)
    registrar_error_business(app, SaldoInsuficiente, 400)
    registrar_error_business(app, MontoInvalido, 400)
    registrar_error_business(app, CategoriaInvalida, 422)
    registrar_error_business(app, UsuarioNotFoundException, 404)
