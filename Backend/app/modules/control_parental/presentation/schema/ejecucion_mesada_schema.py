from datetime import date, datetime
from decimal import Decimal
from pydantic import BaseModel


class EjecucionMesadaResponse(BaseModel):
    id_ejecucion: int
    id_mesada: int
    periodo: str
    monto: Decimal
    fecha_ejecucion: datetime
    id_transaccion_salida: int | None
    id_transaccion_entrada: int | None
    estado: str
    proxima_ejecucion: date | None = None

    class Config:
        from_attributes = True
