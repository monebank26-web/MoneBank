from datetime import datetime, timedelta
from unittest.mock import Mock

import pytest

from app.modules.usuario.application.use_cases.desbloquear_usuario import (
    DesbloquearUsuario,
)
from app.shared.constants.acciones import ACCION_DESBLOQUEAR_USUARIO
from app.shared.constants.codigos_error import CODIGO_CUENTA_NO_BLOQUEADA
from app.shared.constants.estados import (
    ESTADO_ACTIVO,
    ESTADO_BLOQUEADO,
    ESTADO_INACTIVO,
)
from app.shared.exceptions.common import UsuarioNotFoundException
from app.shared.exceptions.usuario_errors import CuentaNoBloqueadaException


def crear_caso_uso(repository=None, registro_repository=None):
    return DesbloquearUsuario(
        repository if repository is not None else Mock(),
        registro_repository if registro_repository is not None else Mock(),
    )


def crear_repository(usuario):
    repository = Mock()
    repository.get_by_id.return_value = usuario
    repository.update.return_value = Mock(
        id_usuario=usuario.id_usuario,
        estado=ESTADO_ACTIVO,
    )
    return repository


def test_desbloquear_bloqueado_actualiza_limpia_y_audita():
    usuario = Mock(
        id_usuario=10,
        estado=ESTADO_BLOQUEADO,
        motivo_bloqueo="Fraude",
        bloqueado_hasta=None,
        contrasena="hash-secreto",
    )
    repository = crear_repository(usuario)
    registro_repository = Mock()
    caso_uso = crear_caso_uso(repository, registro_repository)

    antes = datetime.utcnow()
    resultado = caso_uso.execute(10, id_admin=1)
    despues = datetime.utcnow()

    assert resultado is repository.update.return_value

    datos = repository.update.call_args.args[1]
    assert datos["estado"] == ESTADO_ACTIVO
    assert datos["motivo_bloqueo"] is None
    assert datos["fecha_bloqueo"] is None
    assert antes <= datos["fecha_desbloqueo"] <= despues
    assert datos["intentos_fallidos"] == 0
    assert datos["bloqueado_hasta"] is None

    llamada = registro_repository.registrar.call_args.kwargs
    assert llamada["id_admin"] == 1
    assert llamada["accion"] == ACCION_DESBLOQUEAR_USUARIO
    assert llamada["id_usuario_afectado"] == 10
    assert "BLOQUEADO" in llamada["detalle"]
    assert "Fraude" in llamada["detalle"]
    assert "hash-secreto" not in llamada["detalle"]


def test_desbloquear_inactivo_audita_estado_y_sin_motivo():
    usuario = Mock(
        id_usuario=10,
        estado=ESTADO_INACTIVO,
        motivo_bloqueo=None,
        bloqueado_hasta=None,
    )
    repository = crear_repository(usuario)
    registro_repository = Mock()
    caso_uso = crear_caso_uso(repository, registro_repository)

    caso_uso.execute(10, id_admin=1)

    llamada = registro_repository.registrar.call_args.kwargs
    assert "INACTIVO" in llamada["detalle"]
    assert "Sin motivo" in llamada["detalle"]


def test_desbloquear_activo_con_bloqueo_temporal_vigente():
    usuario = Mock(
        id_usuario=10,
        estado=ESTADO_ACTIVO,
        motivo_bloqueo=None,
        bloqueado_hasta=datetime.now() + timedelta(minutes=5),
    )
    repository = crear_repository(usuario)
    registro_repository = Mock()
    caso_uso = crear_caso_uso(repository, registro_repository)

    caso_uso.execute(10, id_admin=1)

    llamada = registro_repository.registrar.call_args.kwargs
    assert "ACTIVO" in llamada["detalle"]
    assert "bloqueo temporal por intentos fallidos" in llamada["detalle"]


def test_desbloquear_activo_con_bloqueado_hasta_none_lanza_409():
    usuario = Mock(
        id_usuario=10,
        estado=ESTADO_ACTIVO,
        motivo_bloqueo=None,
        bloqueado_hasta=None,
    )
    repository = crear_repository(usuario)
    registro_repository = Mock()
    caso_uso = crear_caso_uso(repository, registro_repository)

    with pytest.raises(CuentaNoBloqueadaException) as excinfo:
        caso_uso.execute(10, id_admin=1)

    assert excinfo.value.code == CODIGO_CUENTA_NO_BLOQUEADA
    assert excinfo.value.message == (
        "La cuenta no se encuentra bloqueada ni desactivada"
    )
    repository.update.assert_not_called()
    registro_repository.registrar.assert_not_called()


def test_desbloquear_activo_con_bloqueo_temporal_vencido_lanza_409():
    usuario = Mock(
        id_usuario=10,
        estado=ESTADO_ACTIVO,
        motivo_bloqueo=None,
        bloqueado_hasta=datetime.now() - timedelta(seconds=1),
    )
    repository = crear_repository(usuario)
    registro_repository = Mock()
    caso_uso = crear_caso_uso(repository, registro_repository)

    with pytest.raises(CuentaNoBloqueadaException):
        caso_uso.execute(10, id_admin=1)

    repository.update.assert_not_called()
    registro_repository.registrar.assert_not_called()


def test_desbloquear_usuario_inexistente_lanza_404():
    repository = Mock()
    repository.get_by_id.return_value = None
    registro_repository = Mock()
    caso_uso = crear_caso_uso(repository, registro_repository)

    with pytest.raises(UsuarioNotFoundException):
        caso_uso.execute(99, id_admin=1)

    repository.update.assert_not_called()
    registro_repository.registrar.assert_not_called()


def test_desbloquear_exige_id_admin():
    caso_uso = crear_caso_uso()

    with pytest.raises(TypeError):
        caso_uso.execute(10)


def test_desbloquear_propaga_el_error_de_auditoria():
    usuario = Mock(
        id_usuario=10,
        estado=ESTADO_BLOQUEADO,
        motivo_bloqueo="Fraude",
        bloqueado_hasta=None,
    )
    repository = crear_repository(usuario)
    registro_repository = Mock()
    registro_repository.registrar.side_effect = RuntimeError("boom")
    caso_uso = crear_caso_uso(repository, registro_repository)

    with pytest.raises(RuntimeError, match="boom"):
        caso_uso.execute(10, id_admin=1)

    repository.update.assert_called_once()
