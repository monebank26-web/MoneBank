from datetime import datetime, timedelta, timezone

import pytest

from app.modules.control_parental.domain.entity.solicitud_control_parental import (
    SolicitudControlParental,
)
from app.shared.exceptions.control_parental_errors import CodigoIntentosAgotados


def construir_solicitud(**overrides):
    datos = {
        "id_solicitud": 1,
        "id_usuario_solicitante": 1,
        "id_usuario_destino": 2,
        "tipo_operacion": SolicitudControlParental.OPERACION_VINCULAR,
        "token_hash": "hash",
        "fecha_expiracion": datetime.now(timezone.utc) + timedelta(hours=1),
        "correo_confirmacion": "padre@example.com",
    }
    datos.update(overrides)
    return SolicitudControlParental(**datos)


def test_esta_vigente_cuando_pendiente_no_usada_y_no_expirada():
    solicitud = construir_solicitud()

    assert solicitud.esta_vigente() is True


def test_no_esta_vigente_si_expiro():
    solicitud = construir_solicitud(
        fecha_expiracion=datetime.now(timezone.utc) - timedelta(hours=1)
    )

    assert solicitud.esta_vigente() is False


def test_no_esta_vigente_si_no_esta_pendiente_o_ya_fue_usada():
    usado = construir_solicitud(usado=True)
    cancelada = construir_solicitud(
        estado=SolicitudControlParental.ESTADO_CANCELADA
    )

    assert usado.esta_vigente() is False
    assert cancelada.esta_vigente() is False


def test_registrar_intento_fallido_incrementa_contador():
    solicitud = construir_solicitud()

    solicitud.registrar_intento_fallido()

    assert solicitud.intentos_fallidos == 1


def test_registrar_intento_fallido_al_llegar_al_maximo_lanza_error():
    solicitud = construir_solicitud(
        intentos_fallidos=SolicitudControlParental.MAX_INTENTOS - 1
    )

    with pytest.raises(CodigoIntentosAgotados):
        solicitud.registrar_intento_fallido()


def test_no_vigente_por_intentos_agotados():
    solicitud = construir_solicitud(
        intentos_fallidos=SolicitudControlParental.MAX_INTENTOS
    )

    assert solicitud.esta_vigente() is False


def test_confirmar_marca_usada_y_confirmada():
    solicitud = construir_solicitud()

    solicitud.confirmar()

    assert solicitud.usado is True
    assert solicitud.estado == SolicitudControlParental.ESTADO_CONFIRMADA


def test_confirmar_solicitud_no_vigente_lanza_value_error():
    solicitud = construir_solicitud(
        fecha_expiracion=datetime.now(timezone.utc) - timedelta(hours=1)
    )

    with pytest.raises(ValueError):
        solicitud.confirmar()


def test_cancelar_marca_usada_y_cancelada():
    solicitud = construir_solicitud()

    solicitud.cancelar()

    assert solicitud.usado is True
    assert solicitud.estado == SolicitudControlParental.ESTADO_CANCELADA
