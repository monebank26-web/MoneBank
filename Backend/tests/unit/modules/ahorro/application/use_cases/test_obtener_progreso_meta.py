from datetime import date, timedelta
from decimal import Decimal
from unittest.mock import Mock

import pytest

from app.modules.ahorro.application.use_cases.obtener_progreso_meta import (
    ObtenerProgresoMeta
)
from app.shared.exceptions.business_exceptions import (
    CuentaNoEncontrada,
    MetaNoEncontrada,
)


def repository_mock():
    repository = Mock()
    cuenta_repository = Mock()

    cuenta = Mock()
    cuenta.id_cuenta = 1
    cuenta_repository.get_cuenta_por_usuario.return_value = cuenta

    ahorro = Mock()
    ahorro.id_ahorro = 46
    ahorro.nombre = "Viaje"
    ahorro.monto_objetivo = Decimal("5000000.00")
    ahorro.saldo_actual = Decimal("2500000.00")
    ahorro.id_cuenta = 1
    ahorro.id_tipo_ahorro = 1
    repository.get_by_id.return_value = ahorro

    tipo_meta = Mock()
    tipo_meta.id_tipo_ahorro = 1
    repository.get_tipo_ahorro.return_value = tipo_meta

    repository.get_progreso.return_value = {
        "porcentaje_avance": Decimal("50.00"),
        "monto_faltante": Decimal("2500000.00"),
    }

    return repository, cuenta_repository


def test_debe_retornar_el_progreso_de_la_meta():

    repository, cuenta_repository = repository_mock()

    resultado = ObtenerProgresoMeta(repository, cuenta_repository).execute(46, 6)

    assert resultado["id_meta"] == 46
    assert resultado["nombre"] == "Viaje"
    assert resultado["monto_objetivo"] == Decimal("5000000.00")
    assert resultado["monto_acumulado"] == Decimal("2500000.00")
    assert resultado["porcentaje_avance"] == Decimal("50.00")
    assert resultado["monto_faltante"] == Decimal("2500000.00")


def test_meta_inexistente_lanza_meta_no_encontrada():

    repository, cuenta_repository = repository_mock()
    repository.get_by_id.return_value = None

    with pytest.raises(MetaNoEncontrada):
        ObtenerProgresoMeta(repository, cuenta_repository).execute(999, 6)


def test_meta_de_otro_usuario_lanza_meta_no_encontrada():

    repository, cuenta_repository = repository_mock()
    repository.get_by_id.return_value.id_cuenta = 99

    with pytest.raises(MetaNoEncontrada):
        ObtenerProgresoMeta(repository, cuenta_repository).execute(46, 6)


def test_ahorro_que_no_es_meta_lanza_meta_no_encontrada():

    repository, cuenta_repository = repository_mock()
    repository.get_tipo_ahorro.return_value.id_tipo_ahorro = 3

    with pytest.raises(MetaNoEncontrada):
        ObtenerProgresoMeta(repository, cuenta_repository).execute(46, 6)


def test_sin_cuenta_lanza_cuenta_no_encontrada():

    repository, cuenta_repository = repository_mock()
    cuenta_repository.get_cuenta_por_usuario.return_value = None

    with pytest.raises(CuentaNoEncontrada):
        ObtenerProgresoMeta(repository, cuenta_repository).execute(46, 6)