from datetime import date
from decimal import Decimal

import pytest

from app.modules.programacion_ahorro.domain.entity.programacion_ahorro import (
    ProgramacionAhorro,
)
from app.shared.exceptions.ahorro_errors import FrecuenciaInvalida


def construir_programacion(
    fecha_inicio,
    frecuencia,
    fecha_cobro=None,
    fecha_fin=None,
    estado="ACTIVA",
):
    return ProgramacionAhorro(
        id_programacion_ahorro=1,
        id_ahorro=5,
        monto_periodico=Decimal("1000.00"),
        fecha_cobro=fecha_cobro or fecha_inicio,
        frecuencia=frecuencia,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        estado=estado,
    )


def test_esta_vencida():
    programacion = construir_programacion(date(2026, 3, 1), "MENSUAL")

    assert programacion.esta_vencida(date(2026, 3, 1))
    assert programacion.esta_vencida(date(2026, 3, 2))
    assert not programacion.esta_vencida(date(2026, 2, 28))


@pytest.mark.parametrize(
    "frecuencia, inicio, cobro, hoy, esperada",
    (
        ("DIARIA", date(2026, 3, 10), date(2026, 3, 17), date(2026, 3, 19), date(2026, 3, 20)),
        ("SEMANAL", date(2026, 3, 2), date(2026, 3, 9), date(2026, 3, 19), date(2026, 3, 23)),
        ("QUINCENAL", date(2026, 3, 1), date(2026, 3, 16), date(2026, 3, 19), date(2026, 3, 31)),
        ("MENSUAL", date(2026, 1, 31), date(2026, 2, 28), date(2026, 3, 19), date(2026, 3, 31)),
        ("MENSUAL", date(2026, 1, 31), date(2026, 2, 28), date(2026, 3, 31), date(2026, 4, 30)),
        ("MENSUAL", date(2026, 1, 30), date(2026, 2, 28), date(2026, 2, 28), date(2026, 3, 30)),
        ("TRIMESTRAL", date(2026, 1, 31), date(2026, 3, 31), date(2026, 4, 15), date(2026, 4, 30)),
        ("SEMESTRAL", date(2026, 1, 31), date(2026, 6, 30), date(2026, 7, 31), date(2027, 1, 31)),
        ("ANUAL", date(2024, 2, 29), date(2025, 2, 28), date(2026, 2, 28), date(2027, 2, 28)),
    ),
)
def test_calcular_proxima_fecha(frecuencia, inicio, cobro, hoy, esperada):
    programacion = construir_programacion(inicio, frecuencia, fecha_cobro=cobro)

    assert programacion.calcular_proxima_fecha(hoy) == esperada


def test_calcular_proxima_fecha_con_frecuencia_invalida():
    programacion = construir_programacion(date(2026, 3, 1), "MENSUAL")
    programacion.frecuencia = "NO_VALIDA"

    with pytest.raises(FrecuenciaInvalida):
        programacion.calcular_proxima_fecha(date(2026, 3, 19))


def test_debe_finalizarse_y_siguiente_estado():
    programacion = construir_programacion(
        date(2026, 1, 31),
        "MENSUAL",
        fecha_fin=date(2026, 3, 31),
    )

    assert programacion.debe_finalizarse(date(2026, 4, 30))
    assert programacion.siguiente_estado(date(2026, 4, 30)) == "FINALIZADA"

    assert not programacion.debe_finalizarse(date(2026, 3, 31))
    assert programacion.siguiente_estado(date(2026, 3, 31)) == "ACTIVA"
