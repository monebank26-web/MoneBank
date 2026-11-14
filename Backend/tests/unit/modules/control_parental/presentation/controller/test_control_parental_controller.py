from unittest.mock import Mock, patch

import pytest
from fastapi import HTTPException

from app.modules.control_parental.presentation.controller.control_parental_controller import (
    ControlParentalController,
)
from app.modules.control_parental.presentation.schema.control_parental_schema import (
    ConfirmarCodigoRequest,
    PermisosUpdate,
    SolicitarVinculacionRequest,
)


def crear_controller():
    return ControlParentalController(Mock(), Mock(), Mock())


@patch(
    "app.modules.control_parental.presentation.controller."
    "control_parental_controller.SolicitarVinculacionUseCase"
)
def test_solicitar_vinculacion_usa_uow_y_commitea(mock_use_case):

    controller = crear_controller()
    current_user = Mock(id_usuario=7)
    data = SolicitarVinculacionRequest(
        nombre_hijo="Ana",
        correo_hijo="ana@correo.com",
    )
    mock_use_case.return_value.execute.return_value = {"codigo": "123456"}

    resultado = controller.solicitar_vinculacion(data, current_user)

    mock_use_case.assert_called_once_with(
        repository=controller.unit_of_work.parentales,
        email_service=controller.email_service,
    )
    mock_use_case.return_value.execute.assert_called_once_with(
        id_padre=7,
        nombre_hijo="Ana",
        correo_hijo="ana@correo.com",
    )
    controller.unit_of_work.commit.assert_called_once()
    assert resultado == {"codigo": "123456"}


@patch(
    "app.modules.control_parental.presentation.controller."
    "control_parental_controller.ObtenerVinculacionesUseCase"
)
def test_obtener_vinculaciones_no_commitea(mock_use_case):

    controller = crear_controller()
    current_user = Mock(id_usuario=7)
    mock_use_case.return_value.execute.return_value = [{"id_control": 1}]

    resultado = controller.obtener_vinculaciones(current_user)

    mock_use_case.assert_called_once_with(controller.repository)
    mock_use_case.return_value.execute.assert_called_once_with(7)
    controller.unit_of_work.commit.assert_not_called()
    assert resultado == [{"id_control": 1}]


@patch(
    "app.modules.control_parental.presentation.controller."
    "control_parental_controller.ActualizarPermisosHijo"
)
def test_actualizar_permisos_usa_uow_y_commitea(mock_use_case):

    controller = crear_controller()
    current_user = Mock(id_usuario=7)
    data = PermisosUpdate(permisos={"puede_gastar": True})
    mock_use_case.return_value.execute.return_value = [{"nombre_permiso": "gastos"}]

    resultado = controller.actualizar_permisos_hijo(3, data, current_user)

    mock_use_case.assert_called_once_with(controller.unit_of_work.parentales)
    mock_use_case.return_value.execute.assert_called_once_with(7, 3, {
        "puede_gastar": True,
    })
    controller.unit_of_work.commit.assert_called_once()
    assert resultado == [{"nombre_permiso": "gastos"}]


@patch(
    "app.modules.control_parental.presentation.controller."
    "control_parental_controller.ConfirmarVinculacionUseCase"
)
def test_confirmar_vinculacion_commitea(mock_use_case):

    controller = crear_controller()
    current_user = Mock(id_usuario=7)
    data = ConfirmarCodigoRequest(codigo="123456")
    mock_use_case.return_value.execute.return_value = {"id_control": 9}

    resultado = controller.confirmar_vinculacion(data, current_user)

    mock_use_case.return_value.execute.assert_called_once_with(7, "123456")
    controller.unit_of_work.commit.assert_called_once()
    assert resultado == {"id_control": 9}


@patch(
    "app.modules.control_parental.presentation.controller."
    "control_parental_controller.ListarHijosParentales"
)
def test_listar_hijos_mapea_error_generico_a_403(mock_use_case):

    controller = crear_controller()
    current_user = Mock(id_usuario=7)
    mock_use_case.return_value.execute.side_effect = ValueError("algo falló")

    with pytest.raises(HTTPException) as excinfo:
        controller.listar_hijos(current_user)

    assert excinfo.value.status_code == 403
    assert excinfo.value.detail == "algo falló"


@patch(
    "app.modules.control_parental.presentation.controller."
    "control_parental_controller.ObtenerResumenHijo"
)
def test_obtener_resumen_hijo_respeta_status_del_error(mock_use_case):

    class ErrorPropio(Exception):
        status_code = 401
        message = "sin acceso al hijo"

    controller = crear_controller()
    current_user = Mock(id_usuario=7)
    mock_use_case.return_value.execute.side_effect = ErrorPropio()

    with pytest.raises(HTTPException) as excinfo:
        controller.obtener_resumen_hijo(3, current_user)

    assert excinfo.value.status_code == 401
    assert excinfo.value.detail == "sin acceso al hijo"
