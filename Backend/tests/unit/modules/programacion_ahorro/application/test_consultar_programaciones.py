from datetime import date
from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from app.modules.programacion_ahorro.application.consultar_programaciones import ConsultarProgramacionesUseCase
from app.shared.exceptions.transaccion_errors import CuentaNoEncontrada


def fila_base(**sobrescritura):
    datos = {
        "id_programacion_ahorro": 1,
        "id_ahorro": 65,
        "id_cuenta": 1,
        "nombre_ahorro": "Viaje",
        "monto_periodico": Decimal("10000.00"),
        "frecuencia": "SEMANAL",
        "fecha_inicio_vigencia": date(2026, 10, 2),
        "fecha_fin_vigencia": date(2026, 10, 17),
        "proxima_fecha_cobro": date(2026, 10, 9),
        "dias_para_proximo_cobro": 5,
        "estado_programacion": "ACTIVA",
    }
    datos.update(sobrescritura)
    return SimpleNamespace(**datos)


def use_case_con_cuenta():
    repository = Mock()

    cuenta = Mock()
    cuenta.id_cuenta = 1
    cuenta_repository = Mock()
    cuenta_repository.get_cuenta_por_usuario.return_value = cuenta

    return ConsultarProgramacionesUseCase(repository, cuenta_repository), repository, cuenta_repository


def test_lista_vigente_mapa_campos():

    caso_uso, repository, cuenta_repository = use_case_con_cuenta()
    repository.obtener_detalles_por_cuenta.return_value = [fila_base()]

    resultado = caso_uso.execute(6)

    assert len(resultado) == 1
    detalle = resultado[0]
    assert detalle.id_programacion_ahorro == 1
    assert detalle.id_ahorro == 65
    assert detalle.nombre_ahorro == "Viaje"
    assert detalle.monto_periodico == Decimal("10000.00")
    assert detalle.frecuencia == "SEMANAL"
    assert detalle.fecha_inicio == date(2026, 10, 2)
    assert detalle.fecha_fin == date(2026, 10, 17)
    assert detalle.fecha_cobro == date(2026, 10, 9)
    assert detalle.tiempo_restante == "En 5 días"
    assert detalle.estado == "ACTIVA"

    cuenta_repository.get_cuenta_por_usuario.assert_called_once_with(6)
    repository.obtener_detalles_por_cuenta.assert_called_once_with(1)


def test_lista_pausada_oculta_fecha_de_cobro():

    caso_uso, repository, _ = use_case_con_cuenta()
    repository.obtener_detalles_por_cuenta.return_value = [
        fila_base(estado_programacion="PAUSADA"),
    ]

    resultado = caso_uso.execute(6)

    assert resultado[0].fecha_cobro is None
    assert resultado[0].tiempo_restante is None
    assert resultado[0].estado == "PAUSADA"


def test_lista_finalizada_oculta_fecha_de_cobro():

    caso_uso, repository, _ = use_case_con_cuenta()
    repository.obtener_detalles_por_cuenta.return_value = [
        fila_base(estado_programacion="FINALIZADA"),
    ]

    resultado = caso_uso.execute(6)

    assert resultado[0].fecha_cobro is None
    assert resultado[0].tiempo_restante is None


def test_dias_cero_devuelve_hoy():

    caso_uso, repository, _ = use_case_con_cuenta()
    repository.obtener_detalles_por_cuenta.return_value = [
        fila_base(dias_para_proximo_cobro=0),
    ]

    resultado = caso_uso.execute(6)

    assert resultado[0].tiempo_restante == "Hoy"
    assert resultado[0].fecha_cobro == date(2026, 10, 9)


def test_dias_un_dia_devuelve_singular():

    caso_uso, repository, _ = use_case_con_cuenta()
    repository.obtener_detalles_por_cuenta.return_value = [
        fila_base(dias_para_proximo_cobro=1),
    ]

    resultado = caso_uso.execute(6)

    assert resultado[0].tiempo_restante == "En 1 día"


def test_dias_negativo_oculta_fecha_de_cobro():

    caso_uso, repository, _ = use_case_con_cuenta()
    repository.obtener_detalles_por_cuenta.return_value = [
        fila_base(dias_para_proximo_cobro=-3),
    ]

    resultado = caso_uso.execute(6)

    assert resultado[0].fecha_cobro is None
    assert resultado[0].tiempo_restante is None


def test_sin_cuenta_lanza_cuenta_no_encontrada():

    caso_uso, repository, cuenta_repository = use_case_con_cuenta()
    cuenta_repository.get_cuenta_por_usuario.return_value = None

    with pytest.raises(CuentaNoEncontrada):
        caso_uso.execute(6)

    repository.obtener_detalles_por_cuenta.assert_not_called()


def test_sin_programaciones_devuelve_lista_vacia():

    caso_uso, repository, _ = use_case_con_cuenta()
    repository.obtener_detalles_por_cuenta.return_value = []

    resultado = caso_uso.execute(6)

    assert resultado == []