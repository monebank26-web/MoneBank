from datetime import date
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


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


class MetaCreate(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100)
    monto_objetivo: Decimal = Field(..., gt=0)
    saldo_inicial: Optional[Decimal] = Field(None, ge=0)
    fecha_objetivo: date
    id_categoria: int


class MetaResponse(BaseModel):
    id_ahorro: int
    nombre: str
    nombre_categoria: Optional[str] = None
    monto_objetivo: Optional[Decimal] = None
    saldo_actual: Optional[Decimal] = None
    porcentaje_completado: Optional[Decimal] = None
    monto_faltante: Optional[Decimal] = None
    fecha_objetivo: Optional[date] = None
    estado: str

    model_config = ConfigDict(from_attributes=True)


class AhorroProgresoResponse(BaseModel):
    id_meta: int
    nombre: str
    monto_objetivo: Optional[Decimal] = None
    monto_acumulado: Optional[Decimal] = None
    porcentaje_avance: Optional[Decimal] = None
    monto_faltante: Optional[Decimal] = None

    model_config = ConfigDict(from_attributes=True)
