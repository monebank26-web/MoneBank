from unittest.mock import Mock

from app.modules.analytics.application.use_cases.obtener_graficas import (
    ObtenerGraficas
)


def test_graficas_generadas_correctamente():
    datos_esperados = {
        "series": [
            {"fecha": "2026-09-03T00:00:00", "tipo_transaccion": "INGRESO", "total": 11010000.0},
        ],
        "totales_por_categoria": [
            {"nombre_categoria": "Salario", "tipo_transaccion": "INGRESO", "total": 10010000.0},
        ],
    }

    repository = Mock()
    repository.obtener_datos_grafica.return_value = datos_esperados

    resultado = ObtenerGraficas(repository).execute(6, None)

    assert resultado == datos_esperados
    repository.obtener_datos_grafica.assert_called_once_with(6, None)


def test_graficas_sin_movimientos_devuelve_listas_vacias():
    datos_vacios = {"series": [], "totales_por_categoria": []}

    repository = Mock()
    repository.obtener_datos_grafica.return_value = datos_vacios

    resultado = ObtenerGraficas(repository).execute(6, None)

    assert resultado["series"] == []
    assert resultado["totales_por_categoria"] == []