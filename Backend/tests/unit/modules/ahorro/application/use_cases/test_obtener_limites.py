from datetime import date, timedelta
from decimal import Decimal
from unittest.mock import Mock

import pytest

from app.modules.ahorro.application.use_cases.obtener_limites import (
    ObtenerLimites,
)
from app.shared.exceptions.business_exceptions import CuentaNoEncontrada


def limite_base():
    limite = Mock()
    limite.id_ahorro = 60
    limite.nombre = "Límite Alimentación (MENSUAL)"
    limite.monto_objetivo = Decimal("10000.00")
    limite.periodo = "MENSUAL"
    limite.estado = "ACTIVO"
    limite.id_categoria = 8
    return limite


def repository_con(limites):
    repository = Mock()

    cuenta = Mock()
    cuenta.id_usuario = 6
    cuenta.id_cuenta = 1
    repository.get_cuenta_por_usuario.return_value = cuenta

    repository.get_by_cuenta_y_tipo.return_value = limites

    categoria = Mock()
    categoria.nombre_categoria = "Alimentación"
    repository.get_categoria.return_value = categoria

    return repository


def test_sin_limites_devuelve_lista_vacia():
    repository = repository_con([])

    resultado = ObtenerLimites(repository).execute(6)

    assert resultado == []


def test_calcula_consumo_del_periodo_mensual():
    repository = repository_con([limite_base()])
    repository.get_gasto_periodo.return_value = Decimal("8500.00")

    resultado = ObtenerLimites(repository).execute(6)

    assert len(resultado) == 1
    fila = resultado[0]
    assert fila["id_ahorro"] == 60
    assert fila["nombre_categoria"] == "Alimentación"
    assert fila["gasto_actual"] == Decimal("8500.00")
    assert fila["porcentaje_usado"] == Decimal("85")
    assert fila["monto_disponible"] == Decimal("1500.00")

    fecha_desde, fecha_hasta = repository.get_gasto_periodo.call_args.args[2:]
    hoy = date.today()
    assert fecha_desde == hoy.replace(day=1)
    assert fecha_hasta == hoy


def test_rango_semanal_arranca_el_lunes_de_esta_semana():
    limite = limite_base()
    limite.periodo = "SEMANAL"
    repository = repository_con([limite])
    repository.get_gasto_periodo.return_value = Decimal("100.00")

    ObtenerLimites(repository).execute(6)

    fecha_desde, _ = repository.get_gasto_periodo.call_args.args[2:]
    hoy = date.today()
    assert fecha_desde == hoy - timedelta(days=hoy.weekday())


def test_omite_filas_con_periodo_invalido():
    limite = limite_base()
    limite.periodo = "ANUAL"
    repository = repository_con([limite])

    resultado = ObtenerLimites(repository).execute(6)

    assert resultado == []
    repository.get_gasto_periodo.assert_not_called()


def test_cuenta_no_existe():
    repository = repository_con([])
    repository.get_cuenta_por_usuario.return_value = None

    with pytest.raises(CuentaNoEncontrada):
        ObtenerLimites(repository).execute(6)
