from unittest.mock import Mock, patch

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.dependencies.repositories import get_unit_of_work
from app.core.security.PasswordHasher import PasswordHasher
from app.modules.auth.presentation.controller.auth_controller import (
    AuthController,
    get_auth_controller,
)
from app.modules.auth.presentation.schema.login_request import LoginRequest
from app.modules.usuario.infrastructure.model.usuario_model import UsuarioModel
from app.shared.exceptions.auth_errors import (
    AccountLockedException,
    CuentaInactivaException,
    InvalidCredentialsException,
)


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


def _assert_login_commitea_ante(excepcion):

    with patch(
        "app.modules.auth.presentation.controller."
        "auth_controller.LoginUsuarioUseCase"
    ) as mock_use_case:
        controller, (_, unit_of_work, _) = controller_con_mocks()
        mock_use_case.return_value.execute.side_effect = excepcion

        with pytest.raises(type(excepcion)):
            controller.login(
                Mock(correo="ana@example.com", contrasena="Secreta123")
            )

        unit_of_work.commit.assert_called_once()
        unit_of_work.rollback.assert_not_called()


def test_login_commitea_ante_credenciales_invalidas():
    _assert_login_commitea_ante(InvalidCredentialsException())


def test_login_commitea_ante_cuenta_bloqueada():
    _assert_login_commitea_ante(AccountLockedException())


def test_login_commitea_ante_cuenta_inactiva():
    _assert_login_commitea_ante(CuentaInactivaException())


def test_login_hace_rollback_ante_excepcion_inesperada():

    with patch(
        "app.modules.auth.presentation.controller."
        "auth_controller.LoginUsuarioUseCase"
    ) as mock_use_case:
        controller, (_, unit_of_work, _) = controller_con_mocks()
        mock_use_case.return_value.execute.side_effect = RuntimeError("boom")

        with pytest.raises(RuntimeError):
            controller.login(
                Mock(correo="ana@example.com", contrasena="Secreta123")
            )

        unit_of_work.rollback.assert_called_once()
        unit_of_work.commit.assert_not_called()


def test_login_fallido_persiste_el_intento_en_sqlite(tmp_path):

    engine = create_engine(f"sqlite:///{tmp_path / 'auth.db'}")
    UsuarioModel.__table__.create(engine)
    session_factory = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )

    sesion = session_factory()
    sesion.add(
        UsuarioModel(
            nombres="Ana",
            apellidos="Perez",
            correo="ana@example.com",
            contrasena=PasswordHasher.hash("Correcta123"),
            estado="ACTIVO",
            id_rol=2,
        )
    )
    sesion.commit()
    sesion.close()

    sesion = session_factory()
    unit_of_work = get_unit_of_work(sesion)
    controller = get_auth_controller(
        unit_of_work=unit_of_work,
        email_service=Mock(),
    )

    with pytest.raises(InvalidCredentialsException):
        controller.login(
            LoginRequest(
                correo="ana@example.com",
                contrasena="Incorrecta123",
            )
        )

    sesion.close()

    sesion = session_factory()
    usuario = (
        sesion.query(UsuarioModel)
        .filter(UsuarioModel.correo == "ana@example.com")
        .one()
    )
    assert usuario.intentos_fallidos == 1
    sesion.close()
