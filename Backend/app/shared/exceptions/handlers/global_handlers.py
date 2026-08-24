from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.responses import ErrorResponse
from app.shared.exceptions.http_exceptions import ValidationException, InternalServerException


def register_global_exception_handlers(app: FastAPI):

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=ValidationException.status_code,
            content=ErrorResponse(message=ValidationException.description).model_dump()
        )

    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=InternalServerException.status_code,
            content=ErrorResponse(message=InternalServerException.description).model_dump()
        )
