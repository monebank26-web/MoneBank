from datetime import date
from unittest.mock import Mock

from app.modules.analytics.application.use_cases.generar_reporte import (
    GenerarReporte
)


def test_reporte_generado_correctamente_con_movimientos():
    repository = Mock()
    repository.obtener_reporte_periodo.return_value = [
        {"nombre_categoria": "Salario", "tipo_transaccion": "INGRESO", "total": 500000.0},
        {"nombre_categoria": "Alimentacion", "tipo_transaccion": "GASTO", "total": 150000.0},
    ]

    resultado = GenerarReporte(repository).execute(
        6, fecha_inicio=date(2026, 8, 1), fecha_fin=date(2026, 8, 31)
    )

    assert resultado["total_ingresos"] == 500000.0
    assert resultado["total_gastos"] == 150000.0
    assert resultado["balance"] == 350000.0
    assert len(resultado["detalle_por_categoria"]) == 2
    repository.obtener_reporte_periodo.assert_called_once_with(
        6, date(2026, 8, 1), date(2026, 8, 31)
    )


def test_datos_del_reporte_coinciden_con_lo_consultado():
    repository = Mock()
    datos_esperados = [
        {"nombre_categoria": "Ventas", "tipo_transaccion": "INGRESO", "total": 1000000.0},
    ]
    repository.obtener_reporte_periodo.return_value = datos_esperados

    resultado = GenerarReporte(repository).execute(
        6, fecha_inicio=date(2026, 8, 1), fecha_fin=date(2026, 8, 31)
    )

    assert resultado["detalle_por_categoria"] == datos_esperados


def test_reporte_sin_movimientos_devuelve_totales_en_cero():
    repository = Mock()
    repository.obtener_reporte_periodo.return_value = []

    resultado = GenerarReporte(repository).execute(
        6, fecha_inicio=date(2026, 8, 1), fecha_fin=date(2026, 8, 31)
    )

    assert resultado["total_ingresos"] == 0
    assert resultado["total_gastos"] == 0
    assert resultado["balance"] == 0
    assert resultado["detalle_por_categoria"] == []


def test_sin_fechas_calcula_el_mes_anterior_finalizado():
    repository = Mock()
    repository.obtener_reporte_periodo.return_value = []

    GenerarReporte(repository).execute(6, periodo="mensual")

    args = repository.obtener_reporte_periodo.call_args.args
    id_usuario, fecha_inicio, fecha_fin = args

    assert id_usuario == 6
    assert fecha_fin < date.today().replace(day=1)
    assert fecha_inicio.day == 1
    assert fecha_inicio.month == fecha_fin.month
