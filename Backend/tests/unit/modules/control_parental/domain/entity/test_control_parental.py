import pytest

from app.modules.control_parental.domain.entity.control_parental import (
    ControlParental,
)
from app.shared.exceptions.control_parental_errors import (
    AutoVinculacionNoPermitida,
    VinculacionDuplicada,
)


def test_crear_inicializa_activo_y_sin_fecha_fin():
    control = ControlParental.crear(id_usuario_parental=1, id_usuario_dependiente=2)

    assert control.estado == ControlParental.ESTADO_ACTIVO
    assert control.permiso_monitoreo is True
    assert control.fecha_inicio is not None
    assert control.fecha_fin is None


def test_autovinculacion_lanza_auto_vinculacion_no_permitida():
    with pytest.raises(AutoVinculacionNoPermitida):
        ControlParental.crear(id_usuario_parental=5, id_usuario_dependiente=5)


def test_estado_invalido_lanza_value_error():
    with pytest.raises(ValueError):
        ControlParental(
            id_control=None,
            id_usuario_parental=1,
            id_usuario_dependiente=2,
            estado="OTRO",
        )


def test_activo_con_fecha_fin_lanza_value_error():
    with pytest.raises(ValueError):
        ControlParental(
            id_control=None,
            id_usuario_parental=1,
            id_usuario_dependiente=2,
            estado=ControlParental.ESTADO_ACTIVO,
            fecha_fin="2026-01-01",
        )


def test_desvincular_finaliza_y_asigna_fecha_fin():
    control = ControlParental.crear(1, 2)

    control.desvincular()

    assert control.estado == ControlParental.ESTADO_FINALIZADO
    assert control.fecha_fin is not None


def test_desvincular_una_vinculacion_inactiva_lanza_vinculacion_duplicada():
    control = ControlParental.crear(1, 2)
    control.desvincular()

    with pytest.raises(VinculacionDuplicada):
        control.desvincular()
