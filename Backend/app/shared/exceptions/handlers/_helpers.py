from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.shared.responses import ErrorResponse


def registrar_error_business(app: FastAPI, exc_tipo: type, status_code: int):
    @app.exception_handler(exc_tipo)
    async def handler_error_business(request: Request, exc: Exception):
        return JSONResponse(
            status_code=status_code,
            content=ErrorResponse(message=str(exc)).model_dump(),
        )

    return handler_error_business