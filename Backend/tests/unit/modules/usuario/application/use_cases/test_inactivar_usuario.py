from unittest.mock import Mock

import pytest

from app.core.security.roles import ROL_ADMIN
from app.modules.usuario.application.use_cases.inactivar_usuario import (
    InactivarUsuario,
)
from app.shared.constants.acciones import ACCION_DESACTIVAR_USUARIO
from app.shared.constants.codigos_error import (
    CODIGO_CUENTA_YA_INACTIVA,
    CODIGO_NO_PUEDE_DESACTIVARSE,
    CODIGO_ULTIMO_ADMINISTRADOR,
)
from app.shared.constants.estados import ESTADO_ACTIVO, ESTADO_INACTIVO
from app.shared.exceptions.common import UsuarioNotFoundException
from app.shared.exceptions.usuario_errors import (
    CuentaYaInactivaException,
    NoPuedeDesactivarseException,
    UltimoAdministradorDesactivacionException,
)


def crear_caso_uso(repository=None, registro_repository=None):
    return InactivarUsuario(
        repository if repository is not None else Mock(),
        registro_repository if registro_repository is not None else Mock(),
    )


def crear_repository(usuario=None):
    repository = Mock()
    if usuario is None:
        usuario = Mock(id_usuario=10, estado=ESTADO_ACTIVO, id_rol=ROL_ADMIN)
    repository.get_by_id.return_value = usuario
    repository.update.return_value = Mock(id_usuario=10, estado=ESTADO_INACTIVO)
    repository.contar_admins_activos.return_value = 2
    return repository


def test_inactivar_usuario_exitoso_desactiva_y_audita_una_vez():

    repository = crear_repository()
    registro_repository = Mock()
    caso_uso = crear_caso_uso(repository, registro_repository)

    resultado = caso_uso.execute(10, id_admin=1)

    assert resultado.estado == ESTADO_INACTIVO
    repository.update.assert_called_once_with(10, {"estado": ESTADO_INACTIVO})
    registro_repository.registrar.assert_called_once()

    llamada = registro_repository.registrar.call_args.kwargs
    assert llamada["id_admin"] == 1
    assert llamada["accion"] == ACCION_DESACTIVAR_USUARIO
    assert llamada["id_usuario_afectado"] == 10


def test_inactivar_usuario_ya_inactivo_lanza_error_propio():

    repository = crear_repository(Mock(id_usuario=10, estado=ESTADO_INACTIVO, id_rol=ROL_ADMIN))
    registro_repository = Mock()
    caso_uso = crear_caso_uso(repository, registro_repository)

    with pytest.raises(CuentaYaInactivaException) as excinfo:
        caso_uso.execute(10, id_admin=1)

    assert excinfo.value.code == CODIGO_CUENTA_YA_INACTIVA
    assert "desactivar" in excinfo.value.message
    repository.update.assert_not_called()
    repository.contar_admins_activos.assert_not_called()
    registro_repository.registrar.assert_not_called()


def test_inactivar_usuario_inexistente_lanza_404():

    repository = crear_repository()
    repository.get_by_id.return_value = None
    caso_uso = crear_caso_uso(repository)

    with pytest.raises(UsuarioNotFoundException):
        caso_uso.execute(99, id_admin=1)


def test_inactivar_usuario_a_si_mismo_lanza_error_propio():

    repository = crear_repository()
    registro_repository = Mock()
    caso_uso = crear_caso_uso(repository, registro_repository)

    with pytest.raises(NoPuedeDesactivarseException) as excinfo:
        caso_uso.execute(10, id_admin=10)

    assert excinfo.value.code == CODIGO_NO_PUEDE_DESACTIVARSE
    assert "desactivar" in excinfo.value.message
    repository.update.assert_not_called()
    registro_repository.registrar.assert_not_called()


def test_inactivar_ultimo_admin_activo_lanza_error_propio():

    repository = crear_repository()
    repository.contar_admins_activos.return_value = 0
    registro_repository = Mock()
    caso_uso = crear_caso_uso(repository, registro_repository)

    with pytest.raises(UltimoAdministradorDesactivacionException) as excinfo:
        caso_uso.execute(10, id_admin=1)

    assert excinfo.value.code == CODIGO_ULTIMO_ADMINISTRADOR
    assert "desactivar" in excinfo.value.message
    repository.update.assert_not_called()
    registro_repository.registrar.assert_not_called()
