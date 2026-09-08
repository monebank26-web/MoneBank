from datetime import date
from decimal import Decimal
from pydantic import BaseModel, Field, model_validator


class MesadaCreate(BaseModel):
    monto: Decimal = Field(gt=0, max_digits=12, decimal_places=2)
    frecuencia: str
    fecha_inicio: date
    fecha_fin: date | None = None

    @model_validator(mode="after")
    def validar_fechas(self):
        if self.fecha_fin and self.fecha_fin < self.fecha_inicio:
            raise ValueError("La fecha final no puede ser anterior a la fecha inicial")
        return self


class MesadaUpdate(BaseModel):
    monto: Decimal | None = Field(default=None, gt=0, max_digits=12, decimal_places=2)
    frecuencia: str | None = None
    fecha_inicio: date | None = None
    fecha_fin: date | None = None
    estado: str | None = None


class MesadaResponse(BaseModel):
    id_mesada: int
    id_control: int
    id_cuenta_padre: int
    id_cuenta_hijo: int
    monto: Decimal
    frecuencia: str
    fecha_inicio: date
    fecha_fin: date | None
    estado: str
    proxima_ejecucion: date | None = None

    class Config:
        from_attributes = True