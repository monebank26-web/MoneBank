from unittest.mock import Mock, patch

from app.modules.auth.presentation.router.router import (
    confirm_password_recovery,
    request_password_recovery,
)


@patch(
    "app.modules.auth.presentation.router.router."
    "RequestPasswordRecoveryUseCase"
)
def test_request_password_recovery_usa_uow_y_commitea(mock_use_case):
    unit_of_work = Mock()
    email_service = Mock()
    request = Mock(correo="ana@example.com")
    mock_use_case.return_value.execute.return_value = {"mensaje": "ok"}

    resultado = request_password_recovery(
        request,
        Mock(),
        unit_of_work,
        email_service,
    )

    mock_use_case.assert_called_once_with(
        unit_of_work.auth,
        unit_of_work.usuarios,
        email_service,
    )
    mock_use_case.return_value.execute.assert_called_once_with(
        "ana@example.com"
    )
    unit_of_work.commit.assert_called_once()
    assert resultado == {"mensaje": "ok"}


@patch(
    "app.modules.auth.presentation.router.router."
    "ConfirmPasswordRecoveryUseCase"
)
def test_confirm_password_recovery_usa_uow_y_commitea(mock_use_case):
    unit_of_work = Mock()
    request = Mock(token="token-123", nueva_contrasena="Nueva123")
    mock_use_case.return_value.execute.return_value = {"mensaje": "ok"}

    resultado = confirm_password_recovery(request, unit_of_work)

    mock_use_case.assert_called_once_with(
        unit_of_work.auth,
        unit_of_work.usuarios,
    )
    mock_use_case.return_value.execute.assert_called_once_with(
        "token-123",
        "Nueva123",
    )
    unit_of_work.commit.assert_called_once()
    assert resultado == {"mensaje": "ok"}
