import logging
from datetime import date
from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import Mock

from app.modules.programacion_ahorro.application.procesar_programaciones_ahorro import (
    ProcesarProgramacionesAhorro,
)
from app.shared.exceptions.common import SaldoInsuficiente

HOY = date(2026, 3, 19)


class UoWFalso:

    def __init__(self, vencidas=None, modelo=None):
        self.programaciones = Mock()
        self.ahorros = Mock()
        self.transacciones = Mock()
        self.commit = Mock()

        self.programaciones.obtener_vencidas.return_value = vencidas or []
        self.programaciones.get_para_procesar.return_value = modelo

        self.ahorros.get_by_id.return_value = SimpleNamespace(
            id_ahorro=47,
            id_cuenta=1,
        )
        self.transacciones.get_cuenta.return_value = SimpleNamespace(
            id_usuario=6,
        )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, traceback):
        return None


def modelo_programacion(**cambios):
    datos = {
        "id_programacion_ahorro": 11,
        "id_ahorro": 47,
        "monto_periodico": Decimal("50000.00"),
        "fecha_cobro": date(2026, 3, 1),
        "frecuencia": "MENSUAL",
        "fecha_inicio": date(2026, 1, 1),
        "fecha_fin": None,
        "estado": "ACTIVA",
    }
    datos.update(cambios)
    return SimpleNamespace(**datos)


def fabrica_uows(*uows):
    creados = list(uows)
    pendientes = list(creados)

    def abrir():
        return pendientes.pop(0)

    return abrir, creados


def construir_caso(modelo, registrar):
    listado = UoWFalso(vencidas=[modelo])
    procesamiento = UoWFalso(modelo=modelo)
    abrir, uows = fabrica_uows(listado, procesamiento)
    reloj = Mock()
    reloj.hoy.return_value = HOY
    caso = ProcesarProgramacionesAhorro(abrir, reloj, lambda _: registrar)
    return caso, abrir, uows


def test_procesa_programacion_vencida_y_actualiza_fecha():
    modelo = modelo_programacion()
    registrar = Mock()
    caso, abrir, uows = construir_caso(modelo, registrar)

    procesadas = caso.execute()

    assert procesadas == 1
    registrar.execute.assert_called_once_with(
        {
            "id_cuenta": 1,
            "id_ahorro": 47,
            "monto": Decimal("50000.00"),
            "fecha": HOY,
            "descripcion": (
                "Ahorro programado con fecha esperada a 2026-03-01"
            ),
        },
        6,
    )
    uows[1].programaciones.actualizar_fecha_cobro.assert_called_once_with(
        11,
        date(2026, 4, 1),
        "ACTIVA",
    )
    uows[1].commit.assert_called_once_with()


def test_finaliza_cuando_la_proxima_fecha_supera_fecha_fin():
    modelo = modelo_programacion(fecha_fin=date(2026, 3, 31))
    registrar = Mock()
    caso, abrir, uows = construir_caso(modelo, registrar)

    caso.execute()

    uows[1].programaciones.actualizar_fecha_cobro.assert_called_once_with(
        11,
        date(2026, 4, 1),
        "FINALIZADA",
    )


def test_saldo_insuficiente_no_actualiza_ni_hace_commit(caplog):
    modelo = modelo_programacion()
    registrar = Mock()
    registrar.execute.side_effect = SaldoInsuficiente()
    caso, abrir, uows = construir_caso(modelo, registrar)

    with caplog.at_level(
        logging.WARNING,
        logger="app.modules.programacion_ahorro.application.procesar_programaciones_ahorro",
    ):
        procesadas = caso.execute()

    assert procesadas == 0
    uows[1].programaciones.actualizar_fecha_cobro.assert_not_called()
    uows[1].commit.assert_not_called()
    assert "Saldo insuficiente para la programación 11" in caplog.text


def test_sin_programaciones_vencidas_no_abre_uow_de_procesamiento():
    listado = UoWFalso(vencidas=[])
    abrir, uows = fabrica_uows(listado)
    reloj = Mock()

    caso = ProcesarProgramacionesAhorro(abrir, reloj, Mock())

    assert caso.execute(hoy=HOY) == 0
    assert len(uows) == 1
    reloj.hoy.assert_not_called()


def test_usa_el_reloj_cuando_no_recibe_hoy():
    modelo = modelo_programacion()
    registrar = Mock()
    caso, abrir, uows = construir_caso(modelo, registrar)

    caso.execute()

    caso.reloj.hoy.assert_called_once_with()
