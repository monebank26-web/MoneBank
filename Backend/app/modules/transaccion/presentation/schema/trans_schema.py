from datetime import date, datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator


class ListaTransaccionesResponse(BaseModel):

    id: int
    tipo: str
    monto: Decimal
    fecha: datetime
    categoria: int
    descripcion: Optional[str] = None

    model_config = ConfigDict(
        from_attributes=True
    )

    @model_validator(mode="before")
    @classmethod
    def desde_modelo(cls, data):
        if hasattr(data, "id_transaccion"):
            return {
                "id": data.id_transaccion,
                "tipo": data.tipo,
                "monto": data.monto,
                "fecha": data.fecha,
                "categoria": data.id_categoria,
                "descripcion": data.descripcion,
            }
        return data


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
