from dataclasses import dataclass
from datetime import date
from decimal import Decimal


FRECUENCIAS_VALIDAS = {"DIARIA", "SEMANAL", "QUINCENAL", "MENSUAL"}
ESTADOS_VALIDOS = {"ACTIVA", "PAUSADA", "FINALIZADA", "CANCELADA"}


@dataclass
class MesadaParental:
    id_mesada: int | None
    id_control: int
    id_cuenta_padre: int
    id_cuenta_hijo: int
    monto: Decimal
    frecuencia: str
    fecha_inicio: date
    fecha_fin: date | None = None
    estado: str = "ACTIVA"

    def validar_creacion(self, saldo_padre: Decimal):
        if self.monto <= Decimal("0"):
            raise ValueError("El monto de la mesada debe ser mayor que cero")
        if self.frecuencia not in FRECUENCIAS_VALIDAS:
            raise ValueError("La frecuencia de la mesada no es válida")
        if self.fecha_fin and self.fecha_fin < self.fecha_inicio:
            raise ValueError("La fecha final no puede ser anterior a la fecha inicial")
        if Decimal(str(saldo_padre or 0)) < self.monto:
            raise ValueError("Saldo insuficiente para asignar la mesada")

    def validar_estado(self):
        if self.estado not in ESTADOS_VALIDOS:
            raise ValueError("El estado de la mesada no es válido")