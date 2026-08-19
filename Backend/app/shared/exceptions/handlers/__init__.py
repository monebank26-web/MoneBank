from fastapi import FastAPI

from app.shared.exceptions.handlers.auth_handlers import (
    register_auth_exception_handlers,
)
from app.shared.exceptions.handlers.usuario_handlers import (
    register_usuario_exception_handlers,
)
from app.shared.exceptions.handlers.transaccion_handlers import (
    register_transaccion_exception_handlers,
)
from app.shared.exceptions.handlers.global_handlers import (
    register_global_exception_handlers,
)


def register_all_exception_handlers(app: FastAPI):
    register_auth_exception_handlers(app)
    register_usuario_exception_handlers(app)
    register_transaccion_exception_handlers(app)
    register_global_exception_handlers(app)
