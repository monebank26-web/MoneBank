from datetime import date
from unittest.mock import Mock

from app.modules.analytics.application.use_cases.obtener_resumen_semanal import (
    ObtenerResumenSemanal
)


def test_resumen_generado_correctamente_con_movimientos():
    repository = Mock()
    repository.obtener_movimientos_periodo.return_value = [
        {"tipo_transaccion": "INGRESO", "total": 1000000.0},
        {"tipo_transaccion": "GASTO", "total": 300000.0},
    ]

    resultado = ObtenerResumenSemanal(repository).execute(
        6, date(2026, 8, 24), date(2026, 8, 30)
    )

    assert resultado["total_ingresos"] == 1000000.0
    assert resultado["total_gastos"] == 300000.0
    assert resultado["balance"] == 700000.0
    assert resultado["tiene_movimientos"] is True
    assert resultado["mensaje"] is None
    repository.obtener_movimientos_periodo.assert_called_once_with(
        6, date(2026, 8, 24), date(2026, 8, 30)
    )


def test_resumen_sin_movimientos_devuelve_mensaje_informativo():
    repository = Mock()
    repository.obtener_movimientos_periodo.return_value = []

    resultado = ObtenerResumenSemanal(repository).execute(
        6, date(2026, 8, 24), date(2026, 8, 30)
    )

    assert resultado["tiene_movimientos"] is False
    assert resultado["total_ingresos"] == 0.0
    assert resultado["total_gastos"] == 0.0
    assert resultado["balance"] == 0.0
    assert resultado["mensaje"] == "No existen movimientos registrados durante esta semana."


def test_calculo_correcto_de_totales_con_varias_transacciones():
    repository = Mock()
    repository.obtener_movimientos_periodo.return_value = [
        {"tipo_transaccion": "INGRESO", "total": 500000.0},
        {"tipo_transaccion": "INGRESO", "total": 200000.0},
        {"tipo_transaccion": "GASTO", "total": 100000.0},
        {"tipo_transaccion": "GASTO", "total": 50000.0},
    ]

    resultado = ObtenerResumenSemanal(repository).execute(
        6, date(2026, 8, 24), date(2026, 8, 30)
    )

    assert resultado["total_ingresos"] == 700000.0
    assert resultado["total_gastos"] == 150000.0
    assert resultado["balance"] == 550000.0


def test_sin_fechas_calcula_la_ultima_semana_finalizada():
    repository = Mock()
    repository.obtener_movimientos_periodo.return_value = []

    ObtenerResumenSemanal(repository).execute(6)

    args = repository.obtener_movimientos_periodo.call_args.args
    id_usuario, fecha_inicio, fecha_fin = args

    assert id_usuario == 6
    assert fecha_fin < date.today()
    assert (fecha_fin - fecha_inicio).days == 6
