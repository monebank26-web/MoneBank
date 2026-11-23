from unittest.mock import Mock

import pytest
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials

from app.core.security import auth
from app.core.security.JwtManager import JwtManager
from app.core.security.roles import ROL_USUARIO
from app.shared.constants.codigos_error import (
    CODIGO_CUENTA_BLOQUEADA,
    CODIGO_CUENTA_INACTIVA,
)
from app.shared.exceptions.auth_errors import (
    CuentaBloqueadaException,
    CuentaInactivaException,
)


def credenciales(token):
    return HTTPAuthorizationCredentials(
        scheme="Bearer",
        credentials=token
    )


def crear_usuario_mock():
    usuario = Mock()
    usuario.id_usuario = 6
    usuario.correo = "bryan@gmail.com"
    usuario.id_rol = ROL_USUARIO
    return usuario


def crear_token(id_usuario):
    return JwtManager.create_token({"sub": str(id_usuario)})


def test_get_current_user_sin_header_rechaza():
    with pytest.raises(HTTPException) as exc:
        auth.get_current_user(credentials=None, repository=Mock())
    assert exc.value.status_code == 401


def test_get_current_user_con_token_invalido_rechaza():
    with pytest.raises(HTTPException) as exc:
        auth.get_current_user(
            credentials=credenciales("token-invalido"),
            repository=Mock()
        )
    assert exc.value.status_code == 401


def test_get_current_user_con_token_valido_devuelve_usuario():
    repository = Mock()
    repository.get_by_id.return_value = crear_usuario_mock()

    token = crear_token(6)
    resultado = auth.get_current_user(
        credentials=credenciales(token),
        repository=repository
    )

    repository.get_by_id.assert_called_once_with(6)
    assert resultado.id_usuario == 6


def test_get_current_user_con_usuario_inexistente_rechaza():
    repository = Mock()
    repository.get_by_id.return_value = None

    token = crear_token(99)
    with pytest.raises(HTTPException) as exc:
        auth.get_current_user(
            credentials=credenciales(token),
            repository=repository
        )
    assert exc.value.status_code == 401


def test_get_current_user_con_usuario_bloqueado_rechaza():
    repository = Mock()
    usuario = crear_usuario_mock()
    usuario.estado = "BLOQUEADO"
    repository.get_by_id.return_value = usuario

    token = crear_token(6)
    with pytest.raises(CuentaBloqueadaException) as exc:
        auth.get_current_user(
            credentials=credenciales(token),
            repository=repository
        )

    assert exc.value.code == CODIGO_CUENTA_BLOQUEADA


def test_get_current_user_con_usuario_inactivo_rechaza():
    repository = Mock()
    usuario = crear_usuario_mock()
    usuario.estado = "INACTIVO"
    repository.get_by_id.return_value = usuario

    token = crear_token(6)
    with pytest.raises(CuentaInactivaException) as exc:
        auth.get_current_user(
            credentials=credenciales(token),
            repository=repository
        )

    assert exc.value.code == CODIGO_CUENTA_INACTIVA


def test_get_current_user_normaliza_el_estado_del_usuario():
    repository = Mock()
    usuario = crear_usuario_mock()
    usuario.estado = " bloqueado "
    repository.get_by_id.return_value = usuario

    token = crear_token(6)
    with pytest.raises(CuentaBloqueadaException):
        auth.get_current_user(
            credentials=credenciales(token),
            repository=repository
        )


def test_get_current_user_con_usuario_activo_permite_el_acceso():
    repository = Mock()
    usuario = crear_usuario_mock()
    usuario.estado = "ACTIVO"
    repository.get_by_id.return_value = usuario

    token = crear_token(6)
    resultado = auth.get_current_user(
        credentials=credenciales(token),
        repository=repository
    )

    assert resultado.id_usuario == 6
