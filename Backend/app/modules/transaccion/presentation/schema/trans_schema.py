from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, model_validator


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
