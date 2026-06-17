from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.modules.usuario.presentation.router import (
    router as usuario_router
)
from app.modules.ahorro.presentation.router import router as ahorro_router
from app.modules.cuenta.presentation.router import (
    router as cuenta_router
)

app = FastAPI(title="MoneBank API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(usuario_router)

@app.get("/")
def root():
    return {"message": "MoneBank funcionando"}


app.include_router(ahorro_router)
app.include_router(cuenta_router)