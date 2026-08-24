from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.modules.usuario.presentation.router.router import (router as usuario_router)
from app.modules.ahorro.presentation.router.router import router as ahorro_router
from app.modules.cuenta.presentation.router.router import (router as cuenta_router)
from app.modules.auth.presentation.router.router import (router as auth_router)
from app.modules.transaccion.presentation.router.router import (
    router as transaccion_router
)

from app.shared.exceptions.handlers import register_all_exception_handlers

app = FastAPI(title="MoneBank API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "MoneBank monenando tu dinero."}


app.include_router(usuario_router)
app.include_router(auth_router)
app.include_router(ahorro_router)
app.include_router(cuenta_router)
app.include_router(transaccion_router)

register_all_exception_handlers(app)
