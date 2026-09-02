from decimal import Decimal
from unittest.mock import Mock

import pytest

from app.modules.ahorro.application.use_cases.obtener_alertas_presupuesto import (
    ObtenerAlertasPresupuesto,
)
from app.shared.exceptions.business_exceptions import CuentaNoEncontrada


def limite_base(estado="ACTIVO", monto=Decimal("10000.00"), periodo="MENSUAL"):
    limite = Mock()
    limite.id_ahorro = 60
    limite.nombre = "Límite Alimentación (MENSUAL)"
    limite.monto_objetivo = monto
    limite.periodo = periodo
    limite.estado = estado
    limite.id_categoria = 8
    return limite


def repository_con(limites, gasto):
    repository = Mock()
    cuenta_repository = Mock()

    cuenta = Mock()
    cuenta.id_usuario = 6
    cuenta.id_cuenta = 1
    cuenta_repository.get_cuenta_por_usuario.return_value = cuenta

    repository.get_by_cuenta_y_tipo.return_value = limites
    repository.get_gasto_periodo.return_value = gasto

    return repository, cuenta_repository


def test_sin_cruces_de_umbral_no_genera_alertas():
    repository, cuenta_repository = repository_con([limite_base()], Decimal("7999.00"))

    alertas = ObtenerAlertasPresupuesto(repository, cuenta_repository).execute(6)

    assert alertas == []


def test_alerta_preventiva_al_alcanzar_el_80_por_ciento():
    repository, cuenta_repository = repository_con([limite_base()], Decimal("8000.00"))

    alertas = ObtenerAlertasPresupuesto(repository, cuenta_repository).execute(6)

    assert len(alertas) == 1
    assert alertas[0]["tipo_alerta"] == "PREVENTIVA"
    assert "80%" in alertas[0]["mensaje"]
    assert "Límite Alimentación (MENSUAL)" in alertas[0]["mensaje"]
    assert alertas[0]["fecha"].year is not None


def test_alerta_limite_superado_por_encima_del_100_por_ciento():
    repository, cuenta_repository = repository_con([limite_base()], Decimal("12500.00"))

    alertas = ObtenerAlertasPresupuesto(repository, cuenta_repository).execute(6)

    assert len(alertas) == 1
    assert alertas[0]["tipo_alerta"] == "LIMITE_SUPERADO"


def test_limites_pausados_no_generan_alertas():
    repository, cuenta_repository = repository_con(
        [limite_base(estado="PAUSADO")], Decimal("9000.00")
    )

    alertas = ObtenerAlertasPresupuesto(repository, cuenta_repository).execute(6)

    assert alertas == []


def test_sin_monto_objetivo_no_genera_alertas():
    repository, cuenta_repository = repository_con([limite_base(monto=None)], Decimal("500.00"))

    alertas = ObtenerAlertasPresupuesto(repository, cuenta_repository).execute(6)

    assert alertas == []


def test_cuenta_no_existe():
    repository, cuenta_repository = repository_con([], Decimal("0"))
    cuenta_repository.get_cuenta_por_usuario.return_value = None

    with pytest.raises(CuentaNoEncontrada):
        ObtenerAlertasPresupuesto(repository, cuenta_repository).execute(6)