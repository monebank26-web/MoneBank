from datetime import date
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator


class ListaTransaccionesResponse(BaseModel):

    id: int
    tipo: str
    monto: Decimal
    fecha: date
    categoria: int
    descripcion: str

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
    referencia: Optional[str] = None
    descripcion: Optional[str] = None
    id_tipo_transaccion: int
    id_cuenta: int
    id_categoria: int
    id_ahorro: Optional[int] = None


class GastoResponse(BaseModel):
    id_transaccion: int
    monto: Decimal
    fecha: date
    referencia: Optional[str] = None
    descripcion: Optional[str] = None
    tipo: str
    id_tipo_transaccion: int
    id_cuenta: int
    id_categoria: int
    id_ahorro: Optional[int] = None

    model_config = ConfigDict(
        from_attributes=True
    )
