from unittest.mock import Mock, patch

from app.modules.auth.presentation.controller.auth_controller import AuthController


def controller_con_mocks():
    repository = Mock()
    unit_of_work = Mock()
    email_service = Mock()
    return AuthController(repository, unit_of_work, email_service), (
        repository,
        unit_of_work,
        email_service,
    )


@patch(
    "app.modules.auth.presentation.controller."
    "auth_controller.RequestPasswordRecoveryUseCase"
)
def test_request_password_recovery_usa_uow_y_commitea(mock_use_case):

    controller, (repository, unit_of_work, email_service) = controller_con_mocks()
    request = Mock(correo="ana@example.com")
    mock_use_case.return_value.execute.return_value = {"mensaje": "ok"}

    resultado = controller.request_password_recovery(request)

    mock_use_case.assert_called_once_with(
        repository,
        unit_of_work.usuarios,
        email_service,
    )
    mock_use_case.return_value.execute.assert_called_once_with("ana@example.com")
    unit_of_work.commit.assert_called_once()
    assert resultado == {"mensaje": "ok"}


@patch(
    "app.modules.auth.presentation.controller."
    "auth_controller.ConfirmPasswordRecoveryUseCase"
)
def test_confirm_password_recovery_usa_uow_y_commitea(mock_use_case):

    controller, (repository, unit_of_work, _) = controller_con_mocks()
    request = Mock(token="token-123", nueva_contrasena="Nueva123")
    mock_use_case.return_value.execute.return_value = {"mensaje": "ok"}

    resultado = controller.confirm_password_recovery(request)

    mock_use_case.assert_called_once_with(repository, unit_of_work.usuarios)
    mock_use_case.return_value.execute.assert_called_once_with(
        "token-123",
        "Nueva123",
    )
    unit_of_work.commit.assert_called_once()
    assert resultado == {"mensaje": "ok"}


@patch(
    "app.modules.auth.presentation.controller."
    "auth_controller.LoginUsuarioUseCase"
)
def test_login_commitea(mock_use_case):

    controller, (repository, unit_of_work, _) = controller_con_mocks()
    request = Mock(correo="ana@example.com", contrasena="Secreta123")
    mock_use_case.return_value.execute.return_value = {"access_token": "abc"}

    resultado = controller.login(request)

    mock_use_case.assert_called_once_with(repository)
    mock_use_case.return_value.execute.assert_called_once_with(
        "ana@example.com",
        "Secreta123",
    )
    unit_of_work.commit.assert_called_once()
    assert resultado == {"access_token": "abc"}


@patch(
    "app.modules.auth.presentation.controller."
    "auth_controller.ActualizarContrasenaUseCase"
)
def test_cambiar_contrasena_usa_id_del_usuario_autenticado(mock_use_case):

    from app.modules.auth.presentation.schema.change_password_request import (
        ContrasenaUpdateRequest,
    )

    controller, (repository, unit_of_work, _) = controller_con_mocks()
    current_user = Mock(id_usuario=7)
    request = ContrasenaUpdateRequest(
        contrasena_actual="Actual123",
        contrasena_nueva="Nueva123!",
    )
    mock_use_case.return_value.execute.return_value = {"mensaje": "ok"}

    resultado = controller.cambiar_contrasena(request, current_user)

    mock_use_case.assert_called_once_with(unit_of_work.usuarios)
    mock_use_case.return_value.execute.assert_called_once_with(
        7,
        "Actual123",
        "Nueva123!",
    )
    unit_of_work.commit.assert_called_once()
    assert resultado == {"mensaje": "ok"}
