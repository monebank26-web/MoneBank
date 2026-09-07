from datetime import datetime
from pydantic import BaseModel

class SerieItem(BaseModel):
    fecha: datetime
    tipo_transaccion: str
    total: float

class CategoriaItem(BaseModel):
    nombre_categoria: str
    tipo_transaccion: str
    total: float

class GraficaResponse(BaseModel):
    series: list[SerieItem]
    totales_por_categoria: list[CategoriaItem]