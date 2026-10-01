from fastapi import FastAPI

from app.shared.exceptions.auth_errors import (
    AccountLockedException,
    EmailAlreadyExistsException,
    EmailNotFoundException,
    InvalidCredentialsException,
    InvalidOrExpiredTokenException,
)
from app.shared.exceptions.handlers._helpers import registrar_error_business


def register_auth_exception_handlers(app: FastAPI):
    registrar_error_business(app, InvalidCredentialsException, 401)
    registrar_error_business(app, AccountLockedException, 423)
    registrar_error_business(app, EmailAlreadyExistsException, 409)
    registrar_error_business(app, EmailNotFoundException, 404)
    registrar_error_business(app, InvalidOrExpiredTokenException, 410)