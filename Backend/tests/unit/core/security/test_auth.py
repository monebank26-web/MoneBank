from unittest.mock import Mock

import pytest
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials

from app.core.security import auth
from app.core.security.JwtManager import JwtManager
from app.core.security.roles import ROL_ADMIN, ROL_USUARIO


def credenciales(token):
    return HTTPAuthorizationCredentials(
        scheme="Bearer",
        credentials=token
    )


def crear_usuario_mock(id_rol):
    usuario = Mock()
    usuario.id_usuario = 6
    usuario.correo = "bryan@gmail.com"
    usuario.id_rol = id_rol
    return usuario


def crear_token(id_usuario):
    return JwtManager.create_token({"sub": str(id_usuario)})


def test_get_current_user_sin_header_rechaza():
    with pytest.raises(HTTPException) as exc:
        auth.get_current_user(credentials=None, db=Mock())
    assert exc.value.status_code == 401


def test_get_current_user_con_token_invalido_rechaza():
    with pytest.raises(HTTPException) as exc:
        auth.get_current_user(
            credentials=credenciales("token-invalido"),
            db=Mock()
        )
    assert exc.value.status_code == 401


def test_get_current_user_con_token_valido_devuelve_usuario(monkeypatch):
    class FakeRepo:
        def __init__(self):
            self.usuario = crear_usuario_mock(ROL_USUARIO)

        def get_by_id(self, db, id_usuario):
            return self.usuario

    fake = FakeRepo()
    monkeypatch.setattr(auth, "SqlUsuarioRepository", lambda: fake)

    token = crear_token(6)
    resultado = auth.get_current_user(
        credentials=credenciales(token),
        db=Mock()
    )

    assert resultado is fake.usuario


def test_get_current_user_con_usuario_inexistente_rechaza(monkeypatch):
    class FakeRepo:
        def get_by_id(self, db, id_usuario):
            return None

    monkeypatch.setattr(auth, "SqlUsuarioRepository", FakeRepo)

    token = crear_token(99)
    with pytest.raises(HTTPException) as exc:
        auth.get_current_user(
            credentials=credenciales(token),
            db=Mock()
        )
    assert exc.value.status_code == 401


def test_require_rol_permite_rol_valido():
    depender = auth.require_rol(ROL_ADMIN)
    resultado = depender(crear_usuario_mock(ROL_ADMIN))
    assert resultado.id_rol == ROL_ADMIN


def test_require_rol_rechaza_rol_no_permitido():
    depender = auth.require_rol(ROL_ADMIN)
    with pytest.raises(HTTPException) as exc:
        depender(crear_usuario_mock(ROL_USUARIO))
    assert exc.value.status_code == 403
