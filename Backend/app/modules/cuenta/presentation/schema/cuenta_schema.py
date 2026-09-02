from datetime import date

from pydantic import BaseModel


class CuentaCreate(BaseModel):
    saldo: float = 0
    estado: str
    id_usuario: int


class CuentaUpdate(BaseModel):
    saldo: float = None
    estado: str = None
    id_usuario: int = None


class CuentaResponse(BaseModel):
    id_cuenta: int
    saldo: float
    estado: str
    id_usuario: int
    fecha_creacion: date = None

    class Config:
        from_attributes = True