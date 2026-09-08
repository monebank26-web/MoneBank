from datetime import date, timedelta
from decimal import Decimal


class EjecucionMesada:
    @staticmethod
    def validar(mesada, saldo_padre: Decimal, fecha: date):
        if mesada.estado != "ACTIVA":
            raise ValueError("La mesada no está activa")
        if fecha < mesada.fecha_inicio:
            raise ValueError("La mesada todavía no puede ejecutarse")
        if mesada.fecha_fin and fecha > mesada.fecha_fin:
            raise ValueError("La mesada ya finalizó")
        if Decimal(str(saldo_padre or 0)) < Decimal(str(mesada.monto)):
            raise ValueError("Saldo insuficiente para ejecutar la mesada")

    @staticmethod
    def periodo(fecha: date) -> str:
        return fecha.isoformat()

    @staticmethod
    def siguiente_fecha(fecha: date, frecuencia: str) -> date:
        dias = {
            "DIARIA": 1,
            "SEMANAL": 7,
            "QUINCENAL": 15,
        }
        if frecuencia == "MENSUAL":
            mes = fecha.month + 1
            anio = fecha.year + (1 if mes == 13 else 0)
            mes = 1 if mes == 13 else mes

            import calendar
            dia = min(fecha.day, calendar.monthrange(anio, mes)[1])
            return date(anio, mes, dia)
        if frecuencia not in dias:
            raise ValueError("La frecuencia de la mesada no es válida")
        return fecha + timedelta(days=dias[frecuencia])
