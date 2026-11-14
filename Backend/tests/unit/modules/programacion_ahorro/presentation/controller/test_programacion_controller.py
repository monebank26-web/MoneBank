from unittest.mock import Mock, patch

from app.modules.programacion_ahorro.presentation.controller.programacion_controller import (
    ProgramacionController,
)


@patch(
    "app.modules.programacion_ahorro.presentation."
    "controller.programacion_controller.CrearProgramacion"
)
def test_crear_programacion_usa_uow_y_commitea(mock_use_case):

    repository = Mock()
    unit_of_work = Mock()
    controller = ProgramacionController(repository, unit_of_work)
    current_user = Mock(id_usuario=7)
    programacion = Mock()
    programacion.model_dump.return_value = {"frecuencia": "MENSUAL"}
    mock_use_case.return_value.execute.return_value = {"id_programacion_ahorro": 3}

    resultado = controller.crear_programacion(programacion, current_user)

    mock_use_case.assert_called_once_with(
        repository,
        unit_of_work.cuentas,
        unit_of_work.ahorros,
    )
    mock_use_case.return_value.execute.assert_called_once_with(
        {"frecuencia": "MENSUAL"},
        7,
    )
    unit_of_work.commit.assert_called_once()
    assert resultado == {"id_programacion_ahorro": 3}


@patch(
    "app.modules.programacion_ahorro.presentation."
    "controller.programacion_controller.ActualizarEstadoUseCase"
)
def test_actualizar_estado_usa_uow_y_commitea(mock_use_case):

    repository = Mock()
    unit_of_work = Mock()
    controller = ProgramacionController(repository, unit_of_work)
    current_user = Mock(id_usuario=7)
    programacion = Mock()
    programacion.id_programacion_ahorro = 5
    programacion.estado = "PAUSADA"
    mock_use_case.return_value.execute.return_value = {"id_programacion_ahorro": 5}

    resultado = controller.actualizar_estado(programacion, current_user)

    mock_use_case.assert_called_once_with(repository, unit_of_work.cuentas)
    mock_use_case.return_value.execute.assert_called_once_with(
        7,
        5,
        "PAUSADA",
    )
    unit_of_work.commit.assert_called_once()
    assert resultado == {"id_programacion_ahorro": 5}


@patch(
    "app.modules.programacion_ahorro.presentation."
    "controller.programacion_controller.ConsultarProgramacionesUseCase"
)
def test_consultar_programaciones_no_commitea(mock_use_case):

    repository = Mock()
    unit_of_work = Mock()
    controller = ProgramacionController(repository, unit_of_work)
    current_user = Mock(id_usuario=7)
    mock_use_case.return_value.execute.return_value = [{"id_programacion_ahorro": 1}]

    resultado = controller.consultar_programaciones(current_user)

    mock_use_case.assert_called_once_with(repository, unit_of_work.cuentas)
    mock_use_case.return_value.execute.assert_called_once_with(7)
    unit_of_work.commit.assert_not_called()
    assert resultado == [{"id_programacion_ahorro": 1}]
