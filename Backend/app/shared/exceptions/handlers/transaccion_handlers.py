from fastapi import FastAPI

from app.shared.exceptions.handlers._helpers import registrar_error_business
from app.shared.exceptions.transaccion_errors import (
    AhorroAsociadoNoValido,
    CategoriaInvalida,
    CuentaNoEncontrada,
    CuentaNoPerteneceAlUsuario,
    FechaInvalida,
    MontoInvalido,
    SaldoInsuficiente,
    TipoTransaccionNoValido,
    TransaccionNoEditable,
    TransaccionesNoEncontrado,
)


def register_transaccion_exception_handlers(app: FastAPI):
    registrar_error_business(app, TransaccionesNoEncontrado, 404)
    registrar_error_business(app, TransaccionNoEditable, 422)
    registrar_error_business(app, MontoInvalido, 400)
    registrar_error_business(app, FechaInvalida, 400)
    registrar_error_business(app, CategoriaInvalida, 422)
    registrar_error_business(app, TipoTransaccionNoValido, 422)
    registrar_error_business(app, AhorroAsociadoNoValido, 422)
    registrar_error_business(app, CuentaNoEncontrada, 404)
    registrar_error_business(app, CuentaNoPerteneceAlUsuario, 403)
    registrar_error_business(app, SaldoInsuficiente, 400)