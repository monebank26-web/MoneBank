from datetime import date, datetime
from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator


class HistorialTransaccionResponse(BaseModel):
    id_usuario: int
    id_cuenta: int
    id_transaccion: int
    tipo_transaccion: str
    monto: Decimal
    fecha: datetime
    referencia: Optional[str] = None
    descripcion: Optional[str] = None
    estado_transaccion: str
    id_tipo_transaccion: int
    id_categoria: Optional[int] = None
    nombre_categoria: Optional[str] = None
    id_ahorro: Optional[int] = None
    nombre_ahorro: Optional[str] = None
    nombre_tipo_ahorro: Optional[str] = None
    nombres: str
    apellidos: str

class HistorialPaginadoResponse(BaseModel):
    items: List[HistorialTransaccionResponse]
    total: int
    pagina: int
    por_pagina: int
    total_paginas: int


class CategoriaResponse(BaseModel):
    id_categoria: int
    nombre_categoria: str


class GastoRequest(BaseModel):
    monto: Decimal = Field(
        ...,
        gt=0,
        description="Monto del gasto, debe ser mayor a 0"
    )
    fecha: date
    descripcion: Optional[str] = None
    id_tipo_transaccion: Optional[int] = None
    id_cuenta: int
    id_categoria: int
    id_ahorro: Optional[int] = Field(None, gt=0)


class GastoResponse(BaseModel):
    id_transaccion: int
    monto: Decimal
    fecha: datetime
    descripcion: Optional[str] = None
    estado: str
    id_tipo_transaccion: int
    id_cuenta: int
    id_categoria: int
    id_ahorro: Optional[int] = None

    model_config = ConfigDict(
        from_attributes=True
    )
