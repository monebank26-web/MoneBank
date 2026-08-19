from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.responses import ErrorResponse
from app.shared.exceptions.business_exceptions import UsuarioNotFoundException


def register_usuario_exception_handlers(app: FastAPI):

    @app.exception_handler(UsuarioNotFoundException)
    async def usuario_not_found_handler(request: Request, exc: UsuarioNotFoundException):
        return JSONResponse(
            status_code=UsuarioNotFoundException.status_code,
            content=ErrorResponse(message=exc.message).model_dump()
        )
