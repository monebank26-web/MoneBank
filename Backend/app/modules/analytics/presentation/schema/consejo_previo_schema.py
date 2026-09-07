from decimal import Decimal
from pydantic import BaseModel, Field


class ConsejoPrevioRequest(BaseModel):
    monto: Decimal = Field(..., gt=0, description="Monto del gasto proyectado")
    id_categoria: int = Field(..., gt=0, description="ID de la categoría del gasto")


class ConsejoPrevioResponse(BaseModel):
    consejo: str
    generado_con_ia: bool
