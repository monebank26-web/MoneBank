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
    descripcion: Optional[str] = None
    estado_transaccion: str
    id_tipo_transaccion: int
    id_categoria: int
    nombre_categoria: str
    id_ahorro: Optional[int] = None
    nombre_ahorro: Optional[str] = None
    nombre_tipo_ahorro: Optional[str] = None
    nombres: str
    apellidos: str

    model_config = ConfigDict(from_attributes=True)


class HistorialRequest(BaseModel):
    pagina: int = Field(1, ge=1)
    por_pagina: int = Field(10, ge=1, le=100)
    ordenar_por: str = Field("fecha", pattern="^(fecha|monto)$")
    orden: str = Field("desc", pattern="^(asc|desc)$")
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None
    monto_min: Optional[float] = None
    monto_max: Optional[float] = None
    busqueda: Optional[str] = Field(None, max_length=100)
    id_tipo_transaccion: Optional[int] = Field(None, gt=0)
    id_categoria: Optional[int] = Field(None, gt=0)

    @model_validator(mode="after")
    def validar_rangos(self):
        if self.fecha_inicio and self.fecha_fin and self.fecha_inicio > self.fecha_fin:
            raise ValueError("fecha_inicio no puede ser mayor a fecha_fin")
        if self.monto_min is not None and self.monto_max is not None and self.monto_min > self.monto_max:
            raise ValueError("monto_min no puede ser mayor a monto_max")
        return self


    
class DetalleTransaccionResponse(BaseModel):
    nombres: str
    apellidos: str
    id_cuenta: int
    id_transaccion: int
    monto: Decimal
    fecha: datetime
    descripcion: Optional[str] = None
    estado_transaccion: str
    id_tipo_transaccion: int
    id_categoria: int
    tipo_transaccion: str
    nombre_categoria: str
    nombre_ahorro: Optional[str] = None
    nombre_tipo_ahorro: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

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


class AbonoAhorroRequest(BaseModel):
    monto: Decimal = Field(
        ...,
        gt=0,
        description="Monto del abono al ahorro, debe ser mayor a 0"
    )
    fecha: date
    descripcion: Optional[str] = None
    id_cuenta: int
    id_ahorro: int = Field(..., gt=0)


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
