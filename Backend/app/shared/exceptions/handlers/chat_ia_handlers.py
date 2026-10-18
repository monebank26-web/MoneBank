from fastapi import FastAPI

from app.shared.exceptions.chat_ia_errors import ChatInvalido, ConsejoIANoDisponible
from app.shared.exceptions.handlers._helpers import registrar_error_business


def register_chat_ia_exception_handlers(app: FastAPI):
    registrar_error_business(app, ChatInvalido, 400)
    registrar_error_business(app, ConsejoIANoDisponible, 503)