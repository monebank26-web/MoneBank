from datetime import datetime
from unittest.mock import Mock

import pytest

from app.core.security.roles import ROL_ADMIN
from app.modules.usuario.application.use_cases.bloquear_usuario import BloquearUsuario
from app.shared.constants.acciones import ACCION_BLOQUEAR_USUARIO
from app.shared.constants.estados import ESTADO_ACTIVO, ESTADO_BLOQUEADO
from app.shared.exceptions.common import UsuarioNotFoundException
from app.shared.exceptions.usuario_errors import (
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


def test_bloquear_usuario_sin_motivo_lanza_422():
    repository = crear_repository()
    caso_uso = crear_caso_uso(repository)

    with pytest.raises(MotivoBloqueoRequeridoException):
        caso_uso.execute(10, "   ")


def test_bloquear_usuario_ya_bloqueada_lanza_409():
    repository = crear_repository(Mock(id_usuario=10, estado="bloqueado", id_rol=ROL_ADMIN))
    caso_uso = crear_caso_uso(repository)

    with pytest.raises(CuentaYaBloqueadaException):
        caso_uso.execute(10, "Motivo valido")


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
        caso_uso.execute(99, "Motivo valido")
