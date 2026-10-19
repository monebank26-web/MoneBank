import asyncio
import json

from fastapi import FastAPI

from app.shared.constants.codigos_error import CODIGO_CORREO_DUPLICADO
from app.shared.exceptions.auth_errors import EmailAlreadyExistsException
from app.shared.exceptions.handlers._helpers import registrar_error_business


def test_correo_duplicado_tiene_codigo_propio():
    """El frontend distingue el 409 de correo repetido por este codigo."""
    assert EmailAlreadyExistsException.code == CODIGO_CORREO_DUPLICADO
    assert EmailAlreadyExistsException().code == CODIGO_CORREO_DUPLICADO


def test_el_handler_409_incluye_el_codigo_en_el_cuerpo():
    app = FastAPI()
    registrar_error_business(app, EmailAlreadyExistsException, 409)

    handler = app.exception_handlers[EmailAlreadyExistsException]
    respuesta = asyncio.run(handler(None, EmailAlreadyExistsException()))

    cuerpo = json.loads(respuesta.body)

    assert respuesta.status_code == 409
    assert cuerpo["message"] == "El correo ya está registrado"
    assert cuerpo["code"] == CODIGO_CORREO_DUPLICADO
