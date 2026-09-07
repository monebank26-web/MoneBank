from datetime import date
from typing import Optional
from pydantic import BaseModel


class ResumenSemanalResponse(BaseModel):
    periodo_inicio: date
    periodo_fin: date
    total_ingresos: float
    total_gastos: float
    balance: float
    tiene_movimientos: bool
    mensaje: Optional[str] = None