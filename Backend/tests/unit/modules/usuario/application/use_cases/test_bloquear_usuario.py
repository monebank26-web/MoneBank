from datetime import datetime
from unittest.mock import Mock

import pytest

from app.core.security.roles import ROL_ADMIN, ROL_USUARIO
from app.modules.usuario.application.use_cases.bloquear_usuario import BloquearUsuario
from app.shared.constants.acciones import ACCION_BLOQUEAR_USUARIO
from app.shared.constants.codigos_error import (
    CODIGO_CUENTA_INACTIVA_NO_BLOQUEABLE,
    CODIGO_CUENTA_YA_BLOQUEADA,
)
from app.shared.constants.estados import (
    ESTADO_ACTIVO,
    ESTADO_BLOQUEADO,
    ESTADO_INACTIVO,
)
from app.shared.exceptions.common import UsuarioNotFoundException
from app.shared.exceptions.usuario_errors import (
    CuentaInactivaNoBloqueableException,
    CuentaYaBloqueadaException,
    MotivoBloqueoRequeridoException,
    NoPuedeBloquearseException,
    UltimoAdministradorException,
)


def crear_caso_uso(repository=None, registro_repository=None):
    return BloquearUsuario(
        repository if repository is not None else Mock(),
        registro_repository if registro_repository is not None else Mock(),
    )


def crear_repository(usuario=None):
    repository = Mock()
    if usuario is None:
        usuario = Mock(id_usuario=10, estado=ESTADO_ACTIVO, id_rol=ROL_ADMIN)
    repository.get_by_id.return_value = usuario
    repository.update.return_value = Mock(id_usuario=10, estado=ESTADO_BLOQUEADO)
    repository.contar_admins_activos.return_value = 2
    return repository


def test_bloquear_usuario_exitoso_bloquea_con_fecha_y_audita():
    repository = crear_repository()
    registro_repository = Mock()
    caso_uso = crear_caso_uso(repository, registro_repository)

    resultado = caso_uso.execute(10, "Fraude detectado", id_admin=1)

    assert resultado.estado == ESTADO_BLOQUEADO
    datos = repository.update.call_args.args[1]
    assert datos["estado"] == ESTADO_BLOQUEADO
    assert datos["motivo_bloqueo"] == "Fraude detectado"
    assert isinstance(datos["fecha_bloqueo"], datetime)

    registro_repository.registrar.assert_called_once()
    llamada = registro_repository.registrar.call_args.kwargs
    assert llamada["id_admin"] == 1
    assert llamada["accion"] == ACCION_BLOQUEAR_USUARIO
    assert llamada["id_usuario_afectado"] == 10
    assert "Fraude detectado" in llamada["detalle"]


def test_bloquear_usuario_no_audita_la_contrasena():
    usuario = Mock(
        id_usuario=10,
        estado=ESTADO_ACTIVO,
        id_rol=ROL_USUARIO,
        contrasena="hash-secreto",
    )
    repository = crear_repository(usuario)
    registro_repository = Mock()
    caso_uso = crear_caso_uso(repository, registro_repository)

    caso_uso.execute(10, "Fraude detectado", id_admin=1)

    llamada = registro_repository.registrar.call_args.kwargs
    assert "hash-secreto" not in llamada["detalle"]


@pytest.mark.parametrize("motivo", [None, "", "   ", "abcd"])
def test_bloquear_usuario_sin_motivo_lanza_422(motivo):
    repository = crear_repository()
    caso_uso = crear_caso_uso(repository)

    with pytest.raises(MotivoBloqueoRequeridoException):
        caso_uso.execute(10, motivo, id_admin=1)


def test_bloquear_usuario_guarda_el_motivo_sin_espacios():
    repository = crear_repository()
    caso_uso = crear_caso_uso(repository)

    caso_uso.execute(10, "  Fraude  ", id_admin=1)

    assert repository.update.call_args.args[1]["motivo_bloqueo"] == "Fraude"


def test_bloquear_usuario_ya_bloqueada_lanza_409():
    repository = crear_repository(Mock(id_usuario=10, estado="bloqueado", id_rol=ROL_ADMIN))
    registro_repository = Mock()
    caso_uso = crear_caso_uso(repository, registro_repository)

    with pytest.raises(CuentaYaBloqueadaException) as excinfo:
        caso_uso.execute(10, "Motivo valido", id_admin=1)

    assert excinfo.value.code == CODIGO_CUENTA_YA_BLOQUEADA
    repository.update.assert_not_called()
    repository.contar_admins_activos.assert_not_called()
    registro_repository.registrar.assert_not_called()


def test_bloquear_usuario_inactivo_lanza_409():
    repository = crear_repository(
        Mock(id_usuario=10, estado=ESTADO_INACTIVO, id_rol=ROL_USUARIO)
    )
    registro_repository = Mock()
    caso_uso = crear_caso_uso(repository, registro_repository)

    with pytest.raises(CuentaInactivaNoBloqueableException) as excinfo:
        caso_uso.execute(10, "Motivo valido", id_admin=1)

    assert excinfo.value.code == CODIGO_CUENTA_INACTIVA_NO_BLOQUEABLE
    assert "bloquear" in excinfo.value.message
    repository.update.assert_not_called()
    repository.contar_admins_activos.assert_not_called()
    registro_repository.registrar.assert_not_called()


def test_bloquear_usuario_a_si_mismo_lanza_400():
    repository = crear_repository()
    caso_uso = crear_caso_uso(repository)

    with pytest.raises(NoPuedeBloquearseException):
        caso_uso.execute(1, "Motivo valido", id_admin=1)


def test_bloquear_ultimo_admin_activo_lanza_409():
    repository = crear_repository(Mock(id_usuario=10, estado=ESTADO_ACTIVO, id_rol=ROL_ADMIN))
    repository.contar_admins_activos.return_value = 0
    caso_uso = crear_caso_uso(repository)

    with pytest.raises(UltimoAdministradorException):
        caso_uso.execute(10, "Motivo valido", id_admin=1)


def test_bloquear_usuario_inexistente_lanza_404():
    repository = crear_repository()
    repository.get_by_id.return_value = None
    caso_uso = crear_caso_uso(repository)

    with pytest.raises(UsuarioNotFoundException):
        caso_uso.execute(99, "Motivo valido", id_admin=1)
