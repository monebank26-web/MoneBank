from unittest.mock import Mock, patch

import pytest
from fastapi import HTTPException

from app.modules.control_parental.presentation.controller.gestionar_mesada_controller import (
    GestionarMesadaController,
)
from app.modules.control_parental.presentation.schema.mesada_parental_schema import (
    MesadaUpdate,
)


def crear_controller():
    return GestionarMesadaController(Mock(), Mock())


@patch(
    "app.modules.control_parental.presentation.controller."
    "gestionar_mesada_controller.GestionarMesada"
)
def test_actualizar_mesada_commitea(mock_use_case):

    controller = crear_controller()
    current_user = Mock(id_usuario=7)
    data = Mock(spec=MesadaUpdate)
    data.model_dump.return_value = {"monto": 75000}
    mock_use_case.return_value.actualizar.return_value = {"id_mesada": 1}

    resultado = controller.actualizar_mesada(3, data, current_user)

    mock_use_case.assert_called_once_with(controller.repository)
    mock_use_case.return_value.actualizar.assert_called_once_with(
        7,
        3,
        {"monto": 75000},
    )
    controller.unit_of_work.commit.assert_called_once()
    assert resultado == {"id_mesada": 1}


@patch(
    "app.modules.control_parental.presentation.controller."
    "gestionar_mesada_controller.GestionarMesada"
)
def test_cancelar_mesada_commitea(mock_use_case):

    controller = crear_controller()
    current_user = Mock(id_usuario=7)
    mock_use_case.return_value.cancelar.return_value = {"id_mesada": 1, "estado": "CANCELADA"}

    resultado = controller.cancelar_mesada(3, current_user)

    mock_use_case.return_value.cancelar.assert_called_once_with(7, 3)
    controller.unit_of_work.commit.assert_called_once()
    assert resultado == {"id_mesada": 1, "estado": "CANCELADA"}


@patch(
    "app.modules.control_parental.presentation.controller."
    "gestionar_mesada_controller.GestionarMesada"
)
def test_actualizar_mesada_permission_error_devuelve_403(mock_use_case):

    controller = crear_controller()
    current_user = Mock(id_usuario=7)
    data = Mock(spec=MesadaUpdate)
    data.model_dump.return_value = {}
    mock_use_case.return_value.actualizar.side_effect = PermissionError(
        "no es tu hijo"
    )

    with pytest.raises(HTTPException) as excinfo:
        controller.actualizar_mesada(3, data, current_user)

    assert excinfo.value.status_code == 403
    assert excinfo.value.detail == "no es tu hijo"
    controller.unit_of_work.commit.assert_not_called()


@patch(
    "app.modules.control_parental.presentation.controller."
    "gestionar_mesada_controller.GestionarMesada"
)
def test_cancelar_mesada_value_error_devuelve_400(mock_use_case):

    controller = crear_controller()
    current_user = Mock(id_usuario=7)
    mock_use_case.return_value.cancelar.side_effect = ValueError("no hay mesada")

    with pytest.raises(HTTPException) as excinfo:
        controller.cancelar_mesada(3, current_user)

    assert excinfo.value.status_code == 400
    assert excinfo.value.detail == "no hay mesada"
    controller.unit_of_work.commit.assert_not_called()
