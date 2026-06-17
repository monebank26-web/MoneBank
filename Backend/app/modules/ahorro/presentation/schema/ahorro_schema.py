from pydantic import BaseModel


class AhorroCreate(BaseModel):
    nombre: str
    monto_objetivo: float
    saldo_inicial: float
    ahorro_automatico: bool
    estado: str
    id_tipo_ahorro: int
    id_categoria: int
    id_cuenta: int


class AhorroResponse(BaseModel):
    id_ahorro: int
    nombre: str
    saldo_actual: float

    class Config:
        from_attributes = True