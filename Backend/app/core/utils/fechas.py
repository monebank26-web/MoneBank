from datetime import date, datetime, timedelta, timezone

ZONA_COLOMBIA = timezone(timedelta(hours=-5))


def hoy_colombia() -> date:
    return datetime.now(ZONA_COLOMBIA).date()


def ahora_colombia() -> datetime:
    return datetime.now(ZONA_COLOMBIA).replace(tzinfo=None)


def fin_del_dia(fecha: date) -> date:
    return fecha + timedelta(days=1)