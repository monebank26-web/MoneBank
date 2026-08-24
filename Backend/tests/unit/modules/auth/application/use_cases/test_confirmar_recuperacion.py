from datetime import datetime, timedelta, timezone
from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from app.modules.auth.application.use_cases.confirm_password_recovery import ConfirmPasswordRecoveryUseCase
from app.shared.exceptions.business_exceptions import InvalidOrExpiredTokenException


def crear_token_valido():
    return SimpleNamespace(
        id=1,
        usuario_id=1,
        token_hash="abc123",
        fecha_expiracion=datetime.now(timezone.utc) + timedelta(minutes=15),
        usado=False,
        esta_expirado=lambda: False,
        fue_utilizado=lambda: False
    )


def crear_token_expirado():
    return SimpleNamespace(
        id=1,
        usuario_id=1,
        token_hash="abc123",
        fecha_expiracion=datetime.now(timezone.utc) - timedelta(minutes=5),
        usado=False,
        esta_expirado=lambda: True,
        fue_utilizado=lambda: False
    )


def crear_token_ya_usado():
    return SimpleNamespace(
        id=1,
        usuario_id=1,
        token_hash="abc123",
        fecha_expiracion=datetime.now(timezone.utc) + timedelta(minutes=15),
        usado=True,
        esta_expirado=lambda: False,
        fue_utilizado=lambda: True
    )


def test_confirmar_recuperacion_exitosa():
    # Arrange
    auth_repository = Mock()
    usuario_repository = Mock()

    auth_repository.find_valid_token.return_value = crear_token_valido()

    use_case = ConfirmPasswordRecoveryUseCase(auth_repository, usuario_repository)

    # Act
    resultado = use_case.execute("token_valido", "MiClave1!")

    # Assert
    assert resultado["mensaje"] == "Contraseña restablecida exitosamente"

    auth_repository.find_valid_token.assert_called_once()
    usuario_repository.update_password.assert_called_once()
    auth_repository.invalidate_token.assert_called_once_with(1)


def test_confirmar_recuperacion_token_no_existe():
    # Arrange
    auth_repository = Mock()
    usuario_repository = Mock()

    auth_repository.find_valid_token.return_value = None

    use_case = ConfirmPasswordRecoveryUseCase(auth_repository, usuario_repository)

    # Act & Assert
    with pytest.raises(InvalidOrExpiredTokenException):
        use_case.execute("token_inexistente", "MiClave1!")

    usuario_repository.update_password.assert_not_called()
    auth_repository.invalidate_token.assert_not_called()


def test_confirmar_recuperacion_token_expirado():
    # Arrange
    auth_repository = Mock()
    usuario_repository = Mock()

    auth_repository.find_valid_token.return_value = crear_token_expirado()

    use_case = ConfirmPasswordRecoveryUseCase(auth_repository, usuario_repository)

    # Act & Assert
    with pytest.raises(InvalidOrExpiredTokenException):
        use_case.execute("token_expirado", "MiClave1!")

    usuario_repository.update_password.assert_not_called()
    auth_repository.invalidate_token.assert_not_called()


def test_confirmar_recuperacion_token_ya_usado():
    # Arrange
    auth_repository = Mock()
    usuario_repository = Mock()

    auth_repository.find_valid_token.return_value = crear_token_ya_usado()

    use_case = ConfirmPasswordRecoveryUseCase(auth_repository, usuario_repository)

    # Act & Assert
    with pytest.raises(InvalidOrExpiredTokenException):
        use_case.execute("token_usado", "MiClave1!")

    usuario_repository.update_password.assert_not_called()
    auth_repository.invalidate_token.assert_not_called()


def test_confirmar_recuperacion_contrasena_invalida():
    # Arrange
    auth_repository = Mock()
    usuario_repository = Mock()

    auth_repository.find_valid_token.return_value = crear_token_valido()

    use_case = ConfirmPasswordRecoveryUseCase(auth_repository, usuario_repository)

    # Act & Assert
    with pytest.raises(ValueError):
        use_case.execute("token_valido", "123")

    usuario_repository.update_password.assert_not_called()
    auth_repository.invalidate_token.assert_not_called()
