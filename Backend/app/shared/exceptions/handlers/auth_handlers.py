from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.responses import ErrorResponse
from app.shared.exceptions.business_exceptions import (
    InvalidCredentialsException,
    AccountLockedException,
    EmailAlreadyExistsException,
    EmailNotFoundException,
    InvalidOrExpiredTokenException,
)


def register_auth_exception_handlers(app: FastAPI):

    @app.exception_handler(InvalidCredentialsException)
    async def invalid_credentials_handler(request: Request, exc: InvalidCredentialsException):
        return JSONResponse(
            status_code=InvalidCredentialsException.status_code,
            content=ErrorResponse(message=exc.message).model_dump()
        )

    @app.exception_handler(AccountLockedException)
    async def account_locked_handler(request: Request, exc: AccountLockedException):
        return JSONResponse(
            status_code=AccountLockedException.status_code,
            content=ErrorResponse(message=exc.message).model_dump()
        )

    @app.exception_handler(EmailAlreadyExistsException)
    async def email_already_exists_handler(request: Request, exc: EmailAlreadyExistsException):
        return JSONResponse(
            status_code=EmailAlreadyExistsException.status_code,
            content=ErrorResponse(message=exc.message).model_dump()
        )

    @app.exception_handler(EmailNotFoundException)
    async def email_not_found_handler(request: Request, exc: EmailNotFoundException):
        return JSONResponse(
            status_code=EmailNotFoundException.status_code,
            content=ErrorResponse(message=exc.message).model_dump()
        )

    @app.exception_handler(InvalidOrExpiredTokenException)
    async def invalid_or_expired_token_handler(request: Request, exc: InvalidOrExpiredTokenException):
        return JSONResponse(
            status_code=InvalidOrExpiredTokenException.status_code,
            content=ErrorResponse(message=exc.message).model_dump()
        )
