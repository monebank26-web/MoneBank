from datetime import date
from pydantic import BaseModel


class DetalleCategoria(BaseModel):
    nombre_categoria: str
    tipo_transaccion: str
    total: float


class ReporteResponse(BaseModel):
    periodo_inicio: date
    periodo_fin: date
    total_ingresos: float
    total_gastos: float
    balance: float
    detalle_por_categoria: list[DetalleCategoria]