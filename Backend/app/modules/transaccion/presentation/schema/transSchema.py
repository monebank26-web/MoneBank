from datetime import date
from typing import Optional

from pydantic import BaseModel


class GastoRequest(BaseModel):
    monto: float
    fecha: date
    referencia: Optional[str] = None
    descripcion: Optional[str] = None
    id_tipo_transaccion: int
    id_cuenta: int
    id_categoria: int
    id_ahorro: Optional[int] = None


class GastoResponse(BaseModel):
    id_transaccion: int
    monto: float
    fecha: date
    referencia: Optional[str] = None
    descripcion: Optional[str] = None
    tipo: str
    id_tipo_transaccion: int
    id_cuenta: int
    id_categoria: int
    id_ahorro: Optional[int] = None

    class Config:
        from_attributes = True