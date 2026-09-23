from decimal import Decimal
from unittest.mock import Mock

import pytest

from app.modules.ahorro.application.use_cases.obtener_resumen_global_metas import (
    ObtenerResumenGlobalMetas,
)
from app.modules.ahorro.domain.entity.ahorro import Ahorro
from app.shared.exceptions.business_exceptions import CuentaNoEncontrada


def crear_meta(monto_objetivo, saldo_actual):
    meta = Mock()
    meta.monto_objetivo = Decimal(monto_objetivo)
    meta.saldo_actual = Decimal(saldo_actual)
    return meta


def _ejecutar(cuenta, metas, id_usuario=6):
    repository = Mock()
    repository.get_by_cuenta_y_tipo.return_value = metas

    cuenta_repository = Mock()
    cuenta_repository.get_cuenta_por_usuario.return_value = cuenta

    resultado = ObtenerResumenGlobalMetas(
        repository, cuenta_repository
    ).execute(id_usuario)

    repository.get_by_cuenta_y_tipo.assert_called_once_with(
        cuenta.id_cuenta, Ahorro.TIPO_META
    )

    return resultado


def test_debe_retornar_resumen_consolidado_de_todas_las_metas():

    cuenta = Mock()
    cuenta.id_cuenta = 1

    metas = [
        crear_meta("1000", "1000"),
        crear_meta("4000", "2000"),
        crear_meta("10000", "3000"),
    ]

    resultado = _ejecutar(cuenta, metas)

    assert resultado["total_ahorrado"] == Decimal("6000")
    assert resultado["monto_objetivo_total"] == Decimal("15000")
    assert resultado["porcentaje_consolidado"] == Decimal("40")
    assert resultado["cantidad_metas"] == 3


def test_porcentaje_consolidado_se_topea_en_100():

    cuenta = Mock()
    cuenta.id_cuenta = 1

    metas = [crear_meta("2000", "4000")]

    resultado = _ejecutar(cuenta, metas)

    assert resultado["porcentaje_consolidado"] == Decimal("100")


def test_sin_metas_retorna_ceros():

    cuenta = Mock()
    cuenta.id_cuenta = 1

    resultado = _ejecutar(cuenta, [])

    assert resultado["total_ahorrado"] == 0
    assert resultado["monto_objetivo_total"] == 0
    assert resultado["porcentaje_consolidado"] == Decimal("0")
    assert resultado["cantidad_metas"] == 0


def test_sin_cuenta_lanza_cuenta_no_encontrada():

    repository = Mock()
    cuenta_repository = Mock()
    cuenta_repository.get_cuenta_por_usuario.return_value = None

    with pytest.raises(CuentaNoEncontrada):
        ObtenerResumenGlobalMetas(repository, cuenta_repository).execute(6)