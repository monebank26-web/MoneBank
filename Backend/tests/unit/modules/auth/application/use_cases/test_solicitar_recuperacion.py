from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from app.modules.auth.application.use_cases.request_password_recovery import RequestPasswordRecoveryUseCase
from app.shared.exceptions.business_exceptions import EmailNotFoundException


def crear_usuario_mock():
    return SimpleNamespace(
        id_usuario=1,
        correo="usuario@test.com"
    )


def test_solicitar_recuperacion_exitosa():
    # Arrange
    auth_repository = Mock()
    usuario_repository = Mock()
    email_service = Mock()

    usuario_repository.get_by_email.return_value = crear_usuario_mock()

    use_case = RequestPasswordRecoveryUseCase(
        auth_repository, usuario_repository, email_service
    )

    # Act
    resultado = use_case.execute("usuario@test.com")

    # Assert
    assert resultado["mensaje"] == (
        "Si el correo está registrado, "
        "recibirás un enlace de recuperación"
    )

    usuario_repository.get_by_email.assert_called_once_with("usuario@test.com")
    auth_repository.invalidate_user_tokens.assert_called_once_with(1)
    auth_repository.create_recovery_token.assert_called_once()
    email_service.send_recovery_email.assert_called_once()


def test_solicitar_recuperacion_correo_no_existe():
    # Arrange
    auth_repository = Mock()
    usuario_repository = Mock()
    email_service = Mock()

    usuario_repository.get_by_email.return_value = None

    use_case = RequestPasswordRecoveryUseCase(
        auth_repository, usuario_repository, email_service
    )

    # Act & Assert
    with pytest.raises(EmailNotFoundException):
        use_case.execute("no@existe.com")

    auth_repository.invalidate_user_tokens.assert_not_called()
    auth_repository.create_recovery_token.assert_not_called()
    email_service.send_recovery_email.assert_not_called()


def test_solicitar_recuperacion_invalida_tokens_viejos():
    # Arrange
    auth_repository = Mock()
    usuario_repository = Mock()
    email_service = Mock()

    usuario_repository.get_by_email.return_value = crear_usuario_mock()

    use_case = RequestPasswordRecoveryUseCase(
        auth_repository, usuario_repository, email_service
    )

    # Act
    use_case.execute("usuario@test.com")

    # Assert
    auth_repository.invalidate_user_tokens.assert_called_once_with(1)


def test_solicitar_recuperacion_envia_email():
    # Arrange
    auth_repository = Mock()
    usuario_repository = Mock()
    email_service = Mock()

    usuario_repository.get_by_email.return_value = crear_usuario_mock()

    use_case = RequestPasswordRecoveryUseCase(
        auth_repository, usuario_repository, email_service
    )

    # Act
    use_case.execute("usuario@test.com")

    # Assert
    email_service.send_recovery_email.assert_called_once()
    args = email_service.send_recovery_email.call_args
    assert args[0][0] == "usuario@test.com"
    assert isinstance(args[0][1], str)
    assert len(args[0][1]) > 0
