from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from app.core.config.settings import settings
from app.core.security.JwtManager import JwtManager
from app.core.security.PasswordHasher import PasswordHasher
from app.modules.auth.application.use_cases.login_usuario import LoginUsuarioUseCase
from app.shared.exceptions.business_exceptions import (
    AccountLockedException,
    InvalidCredentialsException,
)


def crear_usuario():
    return SimpleNamespace(
        id_usuario=1,
        correo="usuario@test.com",
        id_rol=2,
        contrasena=PasswordHasher.hash("password123"),
    )


def test_login_exitoso():
    # Arrange
    repository = Mock()
    repository.login.return_value = crear_usuario()
    repository.is_locked.return_value = False

    use_case = LoginUsuarioUseCase(repository)

    # Act
    resultado = use_case.execute("usuario@test.com", "password123")

    # Assert
    assert resultado["token_type"] == "bearer"
    assert resultado["expires_in"] == settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    assert resultado["usuario_id"] == 1

    payload = JwtManager.decode_token(resultado["access_token"])
    assert payload["sub"] == "1"
    assert payload["correo"] == "usuario@test.com"
    assert payload["id_rol"] == 2

    repository.reset_failed_attempts.assert_called_once_with(1)


def test_login_usuario_no_existe():
    # Arrange
    repository = Mock()
    repository.login.return_value = None

    use_case = LoginUsuarioUseCase(repository)

    # Act & Assert
    with pytest.raises(InvalidCredentialsException):
        use_case.execute("no@existe.com", "password123")

    repository.register_failed_attempt.assert_not_called()


def test_login_contrasena_incorrecta():
    # Arrange
    repository = Mock()
    repository.login.return_value = crear_usuario()
    repository.is_locked.return_value = False

    use_case = LoginUsuarioUseCase(repository)

    # Act & Assert
    with pytest.raises(InvalidCredentialsException):
        use_case.execute("usuario@test.com", "contrasena-incorrecta")

    repository.register_failed_attempt.assert_called_once_with(1)


def test_login_cuenta_bloqueada():
    # Arrange
    repository = Mock()
    repository.login.return_value = crear_usuario()
    repository.is_locked.return_value = True

    use_case = LoginUsuarioUseCase(repository)

    # Act & Assert
    with pytest.raises(AccountLockedException):
        use_case.execute("usuario@test.com", "password123")

    repository.register_failed_attempt.assert_not_called()
