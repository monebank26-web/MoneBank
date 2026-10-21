from unittest.mock import Mock, patch

import pytest
from fastapi import HTTPException

from app.modules.usuario.presentation.controller.usuario_controller import (
    UsuarioController,
)


def mocks():
    return Mock(), Mock()


@patch(
    "app.modules.usuario.presentation.controller."
    "usuario_controller.CrearUsuario"
)
def test_crear_usuario_usa_uow_y_commitea(mock_use_case):

    repository, unit_of_work = mocks()
    controller = UsuarioController(repository, unit_of_work)
    usuario = Mock()
    usuario.model_dump.return_value = {"nombres": "Ana"}
    mock_use_case.return_value.execute.return_value = {"id_usuario": 1}

    resultado = controller.crear_usuario(usuario)

    mock_use_case.assert_called_once_with(repository, unit_of_work.cuentas)
    mock_use_case.return_value.execute.assert_called_once_with({"nombres": "Ana"})
    unit_of_work.commit.assert_called_once()
    assert resultado == {"id_usuario": 1}


@patch(
    "app.modules.usuario.presentation.controller."
    "usuario_controller.ActualizarUsuarioUseCase"
)
def test_actualizar_usuario_commitea(mock_use_case):

    repository, unit_of_work = mocks()
    controller = UsuarioController(repository, unit_of_work)
    current_user = Mock(id_usuario=1)
    usuario = Mock()
    usuario.model_dump.return_value = {"nombres": "Ana"}
    mock_use_case.return_value.execute.return_value = {"id_usuario": 1}

    resultado = controller.actualizar_usuario(1, usuario, current_user)

    mock_use_case.assert_called_once_with(repository)
    unit_of_work.commit.assert_called_once()
    assert resultado == {"id_usuario": 1}


@patch(
    "app.modules.usuario.presentation.controller."
    "usuario_controller.ActualizarUsuarioUseCase"
)
def test_actualizar_usuario_de_otro_lanza_403(mock_use_case):

    repository, unit_of_work = mocks()
    controller = UsuarioController(repository, unit_of_work)
    current_user = Mock(id_usuario=1)

    with pytest.raises(HTTPException) as exc:
        controller.actualizar_usuario(2, Mock(), current_user)

    assert exc.value.status_code == 403
    mock_use_case.assert_not_called()
    unit_of_work.commit.assert_not_called()


@patch(
    "app.modules.usuario.presentation.controller."
    "usuario_controller.EliminarUsuarioUseCase"
)
def test_eliminar_usuario_commitea(mock_use_case):

    repository, unit_of_work = mocks()
    controller = UsuarioController(repository, unit_of_work)
    current_user = Mock(id_usuario=1)
    mock_use_case.return_value.execute.return_value = {"mensaje": "ok"}

    resultado = controller.eliminar_usuario(1, current_user)

    mock_use_case.assert_called_once_with(repository)
    mock_use_case.return_value.execute.assert_called_once_with(1)
    unit_of_work.commit.assert_called_once()
    assert resultado == {"mensaje": "ok"}


@patch(
    "app.modules.usuario.presentation.controller."
    "usuario_controller.BloquearUsuario"
)
def test_bloquear_usuario_envia_motivo(mock_use_case):

    from app.modules.usuario.presentation.schema.usuario_schema import (
        BloqueoUsuarioRequest,
    )

    repository, unit_of_work = mocks()
    controller = UsuarioController(repository, unit_of_work)
    current_user = Mock(id_usuario=1)
    datos = BloqueoUsuarioRequest(motivo="incumplimiento")
    mock_use_case.return_value.execute.return_value = {"estado": "BLOQUEADO"}

    resultado = controller.bloquear_usuario(5, datos, current_user)

    mock_use_case.assert_called_once_with(repository)
    mock_use_case.return_value.execute.assert_called_once_with(5, "incumplimiento")
    unit_of_work.commit.assert_called_once()
    assert resultado == {"estado": "BLOQUEADO"}
