from unittest.mock import Mock, patch

from app.modules.usuario.presentation.router.router import (
    actualizar_usuario,
    crear_usuario,
    eliminar_usuario,
)


@patch(
    "app.modules.usuario.presentation.router.router.CrearUsuario"
)
def test_crear_usuario_usa_uow_y_commitea(mock_use_case):
    unit_of_work = Mock()
    usuario = Mock()
    usuario.model_dump.return_value = {"nombres": "Ana"}
    mock_use_case.return_value.execute.return_value = {"id_usuario": 1}

    resultado = crear_usuario(usuario, unit_of_work)

    mock_use_case.assert_called_once_with(
        unit_of_work.usuarios,
        unit_of_work.cuentas,
    )
    mock_use_case.return_value.execute.assert_called_once_with(
        {"nombres": "Ana"}
    )
    unit_of_work.commit.assert_called_once()
    assert resultado == {"id_usuario": 1}


@patch(
    "app.modules.usuario.presentation.router.router."
    "ActualizarUsuarioUseCase"
)
def test_actualizar_usuario_commitea(mock_use_case):
    unit_of_work = Mock()
    current_user = Mock(id_usuario=1)
    usuario = Mock()
    usuario.model_dump.return_value = {"nombres": "Ana"}
    mock_use_case.return_value.execute.return_value = {"id_usuario": 1}

    resultado = actualizar_usuario(1, usuario, unit_of_work, current_user)

    mock_use_case.assert_called_once_with(unit_of_work.usuarios)
    unit_of_work.commit.assert_called_once()
    assert resultado == {"id_usuario": 1}


@patch(
    "app.modules.usuario.presentation.router.router."
    "EliminarUsuarioUseCase"
)
def test_eliminar_usuario_commitea(mock_use_case):
    unit_of_work = Mock()
    current_user = Mock(id_usuario=1)
    mock_use_case.return_value.execute.return_value = {"mensaje": "ok"}

    resultado = eliminar_usuario(1, unit_of_work, current_user)

    mock_use_case.assert_called_once_with(unit_of_work.usuarios)
    unit_of_work.commit.assert_called_once()
    assert resultado == {"mensaje": "ok"}
