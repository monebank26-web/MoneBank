from pydantic import BaseModel


class CuentaCreate(BaseModel):
    saldo: float = 0
    estado: str
    id_usuario: int


class CuentaResponse(BaseModel):
    id_cuenta: int
    saldo: float
    estado: str
    id_usuario: int

    class Config:
        from_attributes = True