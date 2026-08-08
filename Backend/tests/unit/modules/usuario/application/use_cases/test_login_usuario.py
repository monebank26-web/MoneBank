from unittest.mock import Mock

from app.core.security.JwtManager import JwtManager
from app.core.security.PasswordHasher import PasswordHasher
from app.modules.usuario.application.use_cases.login_usuario import (
    LoginUsuarioUseCase
)


def crear_usuario_mock(contrasena_hash):
    usuario = Mock()
    usuario.id_usuario = 1
    usuario.nombres = "Brayan"
    usuario.apellidos = "Reyes"
    usuario.correo = "bryan@gmail.com"
    usuario.estado = "ACTIVO"
    usuario.id_rol = 1
    usuario.id_tipo_usuario = 1
    usuario.contrasena = contrasena_hash
    return usuario


def test_login_exitoso_devuelve_token_y_usuario():
    repository = Mock()
    db = Mock()

    repository.login.return_value = crear_usuario_mock(
        PasswordHasher.hash("1234")
    )

    resultado = LoginUsuarioUseCase(repository).execute(
        db,
        "bryan@gmail.com",
        "1234"
    )

    assert resultado["success"] is True
    assert "token" in resultado
    assert resultado["usuario"]["correo"] == "bryan@gmail.com"

    payload = JwtManager.decode_token(resultado["token"])
    assert payload["sub"] == "1"


def test_login_con_contrasena_incorrecta_falla():
    repository = Mock()
    db = Mock()

    repository.login.return_value = crear_usuario_mock(
        PasswordHasher.hash("1234")
    )

    resultado = LoginUsuarioUseCase(repository).execute(
        db,
        "bryan@gmail.com",
        "clave-incorrecta"
    )

    assert resultado["success"] is False
    assert "token" not in resultado


def test_login_con_correo_inexistente_falla():
    repository = Mock()
    db = Mock()

    repository.login.return_value = None

    resultado = LoginUsuarioUseCase(repository).execute(
        db,
        "noexiste@gmail.com",
        "1234"
    )

    assert resultado["success"] is False
    assert "token" not in resultado
