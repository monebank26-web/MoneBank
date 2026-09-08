from datetime import date
from decimal import Decimal
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator

Frecuencia = Literal[
    "DIARIA",
    "SEMANAL",
    "QUINCENAL",
    "MENSUAL",
    "TRIMESTRAL",
    "SEMESTRAL",
    "ANUAL",
]

Estado = Literal[
    "ACTIVA",
    "PAUSADA",
    "FINALIZADA",
]


class ProgramacionCreate(BaseModel):
    monto_periodico: Decimal = Field(..., gt=0)
    fecha_cobro: date
    frecuencia: Frecuencia
    fecha_inicio: date
    fecha_fin: Optional[date] = None

    @model_validator(mode="after")
    def validar_fechas(self):
        if self.fecha_fin and self.fecha_fin < self.fecha_inicio:
            raise ValueError(
                "fecha_fin debe ser mayor o igual a fecha_inicio"
            )
        return self


class ProgramacionUpdate(BaseModel):
    id_programacion_ahorro: int
    estado: Estado


class ProgramacionResponse(BaseModel):
    id_programacion_ahorro: int
    monto_periodico: Decimal
    fecha_cobro: date
    frecuencia: str
    fecha_inicio: date
    fecha_fin: Optional[date] = None
    estado: str

    model_config = ConfigDict(from_attributes=True)