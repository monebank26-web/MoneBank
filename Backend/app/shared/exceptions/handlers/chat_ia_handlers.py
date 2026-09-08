from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.responses import ErrorResponse
from app.shared.exceptions.business_exceptions import ChatInvalido


def register_chat_ia_exception_handlers(app: FastAPI):

    @app.exception_handler(ChatInvalido)
    async def chat_invalido_handler(request: Request, exc: ChatInvalido):
        return JSONResponse(
            status_code=ChatInvalido.status_code,
            content=ErrorResponse(message=exc.message).model_dump()
        )
