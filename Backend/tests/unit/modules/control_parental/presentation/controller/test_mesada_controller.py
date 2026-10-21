from unittest.mock import Mock, patch

import pytest
from fastapi import HTTPException

from app.modules.control_parental.presentation.controller.mesada_controller import (
    MesadaController,
)
from app.modules.control_parental.presentation.schema.mesada_parental_schema import (
    MesadaCreate,
)


def crear_controller():
    return MesadaController(Mock(), Mock())


@patch(
    "app.modules.control_parental.presentation.controller."
    "mesada_controller.ConfigurarMesada"
)
def test_crear_mesada_usa_uow_y_commitea(mock_use_case):

    controller = crear_controller()
    current_user = Mock(id_usuario=7)
    data = Mock(spec=MesadaCreate)
    data.model_dump.return_value = {"monto": 50000}
    mock_use_case.return_value.execute.return_value = {"id_mesada": 1}

    resultado = controller.crear_mesada(3, data, current_user)

    mock_use_case.assert_called_once_with(controller.unit_of_work.mesadas)
    mock_use_case.return_value.execute.assert_called_once_with(
        7,
        3,
        {"monto": 50000},
    )
    controller.unit_of_work.commit.assert_called_once()
    assert resultado == {"id_mesada": 1}


@patch(
    "app.modules.control_parental.presentation.controller."
    "mesada_controller.ObtenerMesada"
)
def test_obtener_mesada_no_commitea(mock_use_case):

    controller = crear_controller()
    current_user = Mock(id_usuario=7)
    mock_use_case.return_value.execute.return_value = {"id_mesada": 1}

    resultado = controller.obtener_mesada(3, current_user)

    mock_use_case.assert_called_once_with(controller.repository)
    mock_use_case.return_value.execute.assert_called_once_with(7, 3)
    controller.unit_of_work.commit.assert_not_called()
    assert resultado == {"id_mesada": 1}


@patch(
    "app.modules.control_parental.presentation.controller."
    "mesada_controller.ConfigurarMesada"
)
def test_crear_mesada_mapea_error_a_http_exception(mock_use_case):

    controller = crear_controller()
    current_user = Mock(id_usuario=7)
    data = Mock(spec=MesadaCreate)
    data.model_dump.return_value = {"monto": 50000}
    mock_use_case.return_value.execute.side_effect = ValueError("mesada inválida")

    with pytest.raises(HTTPException) as excinfo:
        controller.crear_mesada(3, data, current_user)

    assert excinfo.value.status_code == 403
    assert excinfo.value.detail == "mesada inválida"
    controller.unit_of_work.commit.assert_not_called()
