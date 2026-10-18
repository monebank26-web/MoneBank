from datetime import date

import pytest

from app.modules.ahorro.domain.entity.ahorro import Ahorro


def construir_ahorro(**overrides):
    datos = {
        "id_ahorro": 1,
        "nombre": "Viaje",
        "monto_objetivo": 1000000,
        "saldo_actual": 250000,
        "estado": Ahorro.ESTADO_ACTIVO,
        "fecha_objetivo": date(2027, 1, 1),
        "periodo": Ahorro.PERIODO_MENSUAL,
    }
    datos.update(overrides)
    return Ahorro(**datos)


def test_es_meta_y_es_limite():
    ahorro = construir_ahorro()

    assert ahorro.es_meta(Ahorro.TIPO_META) is True
    assert ahorro.es_meta(Ahorro.TIPO_LIMITE) is False
    assert ahorro.es_limite(Ahorro.TIPO_LIMITE) is True


def test_calcular_porcentaje_avance():
    ahorro = construir_ahorro(saldo_actual=500000, monto_objetivo=1000000)

    assert ahorro.calcular_porcentaje_avance() == 50


def test_calcular_porcentaje_avance_sin_objetivo_retorna_cero():
    assert construir_ahorro(monto_objetivo=0).calcular_porcentaje_avance() == 0


def test_calcular_dinero_faltante():
    ahorro = construir_ahorro(saldo_actual=250000, monto_objetivo=1000000)

    assert ahorro.calcular_dinero_faltante() == 750000


def test_calcular_dinero_faltante_no_es_negativo():
    ahorro = construir_ahorro(saldo_actual=1200000, monto_objetivo=1000000)

    assert ahorro.calcular_dinero_faltante() == 0


def test_calcular_dinero_faltante_sin_objetivo_retorna_cero():
    assert construir_ahorro(monto_objetivo=0).calcular_dinero_faltante() == 0


def test_esta_en_alerta_en_el_umbral():
    ahorro = construir_ahorro()

    assert ahorro.esta_en_alerta(80) is True
    assert ahorro.esta_en_alerta(79) is False


def test_es_fecha_objetivo_valida():
    ahorro = construir_ahorro(fecha_objetivo=date(2027, 1, 1))

    assert ahorro.es_fecha_objetivo_valida(date(2026, 1, 1)) is True
    assert ahorro.es_fecha_objetivo_valida(date(2028, 1, 1)) is False


def test_es_fecha_objetivo_valida_sin_fecha_retorna_false():
    assert construir_ahorro(fecha_objetivo=None).es_fecha_objetivo_valida() is False


def test_es_periodo_valido():
    assert Ahorro.es_periodo_valido(Ahorro.PERIODO_DIARIO) is True
    assert Ahorro.es_periodo_valido(Ahorro.PERIODO_SEMANAL) is True
    assert Ahorro.es_periodo_valido(Ahorro.PERIODO_MENSUAL) is True
    assert Ahorro.es_periodo_valido("ANUAL") is False


def test_calcular_rango_periodo_diario():
    fecha = date(2026, 1, 5)

    assert Ahorro.calcular_rango_periodo(Ahorro.PERIODO_DIARIO, fecha) == (
        fecha,
        fecha,
    )


def test_calcular_rango_periodo_mensual_inicia_en_dia_uno():
    fecha = date(2026, 1, 15)

    assert Ahorro.calcular_rango_periodo(Ahorro.PERIODO_MENSUAL, fecha) == (
        date(2026, 1, 1),
        fecha,
    )


def test_calcular_rango_periodo_semanal_inicia_en_lunes():
    fecha = date(2026, 1, 8)
    inicio, fin = Ahorro.calcular_rango_periodo(Ahorro.PERIODO_SEMANAL, fecha)

    assert inicio.weekday() == 0
    assert fin == fecha


def test_calcular_rango_periodo_invalido_retorna_none():
    assert Ahorro.calcular_rango_periodo("ANUAL", date(2026, 1, 1)) is None
