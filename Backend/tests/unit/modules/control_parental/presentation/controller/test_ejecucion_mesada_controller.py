from datetime import date
from unittest.mock import Mock, patch

import pytest
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError

from app.modules.control_parental.presentation.controller.ejecucion_mesada_controller import (
    EjecucionMesadaController,
)


def crear_controller():
    return EjecucionMesadaController(Mock(), Mock())


def crear_ejecucion():
    ejecucion = Mock()
    ejecucion.id_ejecucion = 11
    ejecucion.id_mesada = 5
    ejecucion.monto = 50000
    ejecucion.periodo = "2026-10"
    ejecucion.id_transaccion_salida = 21
    ejecucion.id_transaccion_entrada = 22
    ejecucion.estado = "EJECUTADA"
    return ejecucion


@patch(
    "app.modules.control_parental.presentation.controller."
    "ejecucion_mesada_controller.EjecutarMesada"
)
def test_ejecutar_mesada_retorna_payload_y_commitea(mock_use_case):

    controller = crear_controller()
    current_user = Mock(id_usuario=7)
    proxima = date(2026, 11, 1)
    mock_use_case.return_value.execute.return_value = (crear_ejecucion(), proxima)

    resultado = controller.ejecutar_mesada(3, current_user, date(2026, 10, 1))

    mock_use_case.assert_called_once_with(controller.repository)
    mock_use_case.return_value.execute.assert_called_once_with(
        7,
        3,
        date(2026, 10, 1),
    )
    controller.unit_of_work.commit.assert_called_once()
    assert resultado["mensaje"] == "Mesada ejecutada correctamente"
    assert resultado["id_ejecucion"] == 11
    assert resultado["proxima_ejecucion"] == proxima


@patch(
    "app.modules.control_parental.presentation.controller."
    "ejecucion_mesada_controller.EjecutarMesada"
)
def test_ejecutar_mesada_permission_error_hace_rollback_y_403(mock_use_case):

    controller = crear_controller()
    current_user = Mock(id_usuario=7)
    mock_use_case.return_value.execute.side_effect = PermissionError("no autorizado")

    with pytest.raises(HTTPException) as excinfo:
        controller.ejecutar_mesada(3, current_user)

    controller.unit_of_work.rollback.assert_called_once()
    controller.unit_of_work.commit.assert_not_called()
    assert excinfo.value.status_code == 403
    assert excinfo.value.detail == "no autorizado"


@patch(
    "app.modules.control_parental.presentation.controller."
    "ejecucion_mesada_controller.EjecutarMesada"
)
def test_ejecutar_mesada_value_error_hace_rollback_y_400(mock_use_case):

    controller = crear_controller()
    current_user = Mock(id_usuario=7)
    mock_use_case.return_value.execute.side_effect = ValueError("mesada vencida")

    with pytest.raises(HTTPException) as excinfo:
        controller.ejecutar_mesada(3, current_user)

    controller.unit_of_work.rollback.assert_called_once()
    controller.unit_of_work.commit.assert_not_called()
    assert excinfo.value.status_code == 400
    assert excinfo.value.detail == "mesada vencida"


@patch(
    "app.modules.control_parental.presentation.controller."
    "ejecucion_mesada_controller.EjecutarMesada"
)
def test_ejecutar_mesada_error_bd_hace_rollback_y_500(mock_use_case):

    controller = crear_controller()
    current_user = Mock(id_usuario=7)
    mock_use_case.return_value.execute.side_effect = SQLAlchemyError("boom")

    with pytest.raises(HTTPException) as excinfo:
        controller.ejecutar_mesada(3, current_user)

    controller.unit_of_work.rollback.assert_called_once()
    controller.unit_of_work.commit.assert_not_called()
    assert excinfo.value.status_code == 500
    assert "transacciones de la mesada" in excinfo.value.detail
