from unittest.mock import Mock

import pytest
from fastapi import HTTPException

from app.core.security import auth
from app.core.security.roles import ROL_ADMIN, ROL_USUARIO


def crear_usuario_mock(id_rol):
    usuario = Mock()
    usuario.id_usuario = 6
    usuario.correo = "bryan@gmail.com"
    usuario.id_rol = id_rol
    return usuario


def test_require_rol_permite_rol_valido():
    depender = auth.require_rol(ROL_ADMIN)
    resultado = depender(crear_usuario_mock(ROL_ADMIN))
    assert resultado.id_rol == ROL_ADMIN


def test_require_rol_rechaza_rol_no_permitido():
    depender = auth.require_rol(ROL_ADMIN)
    with pytest.raises(HTTPException) as exc:
        depender(crear_usuario_mock(ROL_USUARIO))
    assert exc.value.status_code == 403
