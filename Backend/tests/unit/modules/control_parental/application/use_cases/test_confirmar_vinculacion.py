from datetime import datetime, timedelta, timezone
from unittest.mock import Mock

import pytest

from app.modules.control_parental.application.use_cases._servicios import (
    hash_codigo,
)
from app.modules.control_parental.application.use_cases.confirmar_vinculacion import (
    ConfirmarVinculacionUseCase,
)
from app.modules.control_parental.domain.entity.solicitud_control_parental import (
    SolicitudControlParental,
)
from app.shared.exceptions.control_parental_errors import (
    CodigoInvalido,
    VinculacionDuplicada,
)


def construir_solicitud(id_solicitante=7, id_destino=8):
    return SolicitudControlParental(
        id_solicitud=1,
        id_usuario_solicitante=id_solicitante,
        id_usuario_destino=id_destino,
        tipo_operacion=SolicitudControlParental.OPERACION_VINCULAR,
        token_hash=hash_codigo("123456"),
        fecha_expiracion=datetime.now(timezone.utc) + timedelta(minutes=15),
        correo_confirmacion="hijo@example.com",
    )


def crear_caso(solicitud, vinculacion_activa=None):
    repository = Mock()
    repository.buscar_solicitud_vigente.return_value = solicitud
    repository.buscar_vinculacion_activa.return_value = vinculacion_activa
    repository.guardar_vinculacion.return_value = {"id_control": 9}
    return ConfirmarVinculacionUseCase(repository), repository


def test_confirma_con_el_padre_que_pidio_el_codigo():
    solicitud = construir_solicitud()
    caso, repository = crear_caso(solicitud)

    resultado = caso.execute(7, "123456")

    repository.buscar_solicitud_vigente.assert_called_once_with(
        hash_codigo("123456"),
        SolicitudControlParental.OPERACION_VINCULAR,
    )
    repository.buscar_vinculacion_activa.assert_called_once_with(7, 8)
    assert solicitud.usado is True
    assert solicitud.estado == SolicitudControlParental.ESTADO_CONFIRMADA
    repository.actualizar_solicitud.assert_called_once_with(solicitud)
    vinculacion = repository.guardar_vinculacion.call_args.args[0]
    assert vinculacion.id_usuario_parental == 7
    assert vinculacion.id_usuario_dependiente == 8
    assert resultado == {"id_control": 9}


def test_rechaza_codigo_de_otra_solicitud():
    solicitud = construir_solicitud(id_solicitante=99)
    caso, repository = crear_caso(solicitud)

    with pytest.raises(CodigoInvalido):
        caso.execute(7, "123456")

    repository.actualizar_solicitud.assert_not_called()
    repository.guardar_vinculacion.assert_not_called()


def test_rechaza_cuando_no_hay_solicitud_vigente():
    caso, repository = crear_caso(None)

    with pytest.raises(CodigoInvalido):
        caso.execute(7, "123456")

    repository.guardar_vinculacion.assert_not_called()


def test_vinculacion_duplicada_cancela_solicitud():
    solicitud = construir_solicitud()
    caso, repository = crear_caso(solicitud, vinculacion_activa=Mock())

    with pytest.raises(VinculacionDuplicada):
        caso.execute(7, "123456")

    assert solicitud.usado is True
    assert solicitud.estado == SolicitudControlParental.ESTADO_CANCELADA
    repository.guardar_vinculacion.assert_not_called()
