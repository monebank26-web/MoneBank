from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.modules.usuario.presentation.router.router import (router as usuario_router)
from app.modules.ahorro.presentation.router.router import router as ahorro_router
from app.modules.cuenta.presentation.router.router import (router as cuenta_router)
from app.modules.auth.presentation.router.router import (router as auth_router)

from app.core.responses import ErrorResponse
from app.shared.exceptions.business_exceptions import (
    AccountLockedException,
    EmailAlreadyExistsException,
    InvalidCredentialsException,
)
from app.shared.exceptions.http_exceptions import ValidationException, InternalServerException

app = FastAPI(title="MoneBank API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(usuario_router)
app.include_router(auth_router)

@app.get("/")
def root():
    return {"message": "MoneBank funcionando"}


app.include_router(ahorro_router)
app.include_router(cuenta_router)

@app.exception_handler(InvalidCredentialsException)
def invalid_credentials_handler(request: Request, exc: InvalidCredentialsException):
    return JSONResponse(
        status_code=InvalidCredentialsException.status_code,
        content=ErrorResponse(message=exc.message).model_dump()
    )


@app.exception_handler(AccountLockedException)
def account_locked_handler(request: Request, exc: AccountLockedException):
    return JSONResponse(
        status_code=AccountLockedException.status_code,
        content=ErrorResponse(message=exc.message).model_dump()
    )


@app.exception_handler(EmailAlreadyExistsException)
def email_already_exists_handler(request: Request, exc: EmailAlreadyExistsException):
    return JSONResponse(
        status_code=EmailAlreadyExistsException.status_code,
        content=ErrorResponse(message=exc.message).model_dump()
    )


@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=ValidationException.status_code,
        content=ErrorResponse(message=ValidationException.description).model_dump()
    )


@app.exception_handler(Exception)
def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=InternalServerException.status_code,
        content=ErrorResponse(message=InternalServerException.description).model_dump()
    )