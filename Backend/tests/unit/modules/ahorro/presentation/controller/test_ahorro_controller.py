from unittest.mock import Mock, patch

from app.modules.ahorro.presentation.controller.ahorro_controller import (
    AhorroController,
)


@patch(
    "app.modules.ahorro.presentation.controller."
    "ahorro_controller.RegistrarAbonoAhorro"
)
@patch(
    "app.modules.ahorro.presentation.controller."
    "ahorro_controller.CrearMeta"
)
def test_crear_meta_usa_uow_y_commitea(mock_use_case, mock_abono):

    repository = Mock()
    unit_of_work = Mock()
    controller = AhorroController(repository, unit_of_work)
    current_user = Mock(id_usuario=7)
    meta = Mock()
    meta.model_dump.return_value = {"nombre": "Viaje"}
    mock_use_case.return_value.execute.return_value = {"id_ahorro": 1}

    resultado = controller.crear_meta(meta, current_user)

    mock_abono.assert_called_once_with(unit_of_work.transacciones)
    mock_use_case.assert_called_once_with(
        repository,
        unit_of_work.cuentas,
        mock_abono.return_value,
    )
    mock_use_case.return_value.execute.assert_called_once_with(
        {"nombre": "Viaje"},
        7,
    )
    unit_of_work.commit.assert_called_once()
    assert resultado == {"id_ahorro": 1}


@patch(
    "app.modules.ahorro.presentation.controller."
    "ahorro_controller.ObtenerMetas"
)
def test_obtener_metas_no_commitea(mock_use_case):

    repository = Mock()
    unit_of_work = Mock()
    controller = AhorroController(repository, unit_of_work)
    current_user = Mock(id_usuario=7)
    mock_use_case.return_value.execute.return_value = [{"id_ahorro": 1}]

    resultado = controller.obtener_metas(current_user)

    mock_use_case.assert_called_once_with(repository, unit_of_work.cuentas)
    mock_use_case.return_value.execute.assert_called_once_with(7)
    unit_of_work.commit.assert_not_called()
    assert resultado == [{"id_ahorro": 1}]


@patch(
    "app.modules.ahorro.presentation.controller."
    "ahorro_controller.ActualizarAhorroUseCase"
)
def test_actualizar_ahorro_commitea(mock_use_case):

    repository = Mock()
    unit_of_work = Mock()
    controller = AhorroController(repository, unit_of_work)
    current_user = Mock(id_usuario=7)
    ahorro = Mock()
    ahorro.model_dump.return_value = {"nombre": "Viaje"}
    mock_use_case.return_value.execute.return_value = {"id_ahorro": 9}

    resultado = controller.actualizar_ahorro(9, ahorro, current_user)

    mock_use_case.assert_called_once_with(repository, unit_of_work.cuentas)
    mock_use_case.return_value.execute.assert_called_once_with(
        9,
        {"nombre": "Viaje"},
        7,
    )
    unit_of_work.commit.assert_called_once()
    assert resultado == {"id_ahorro": 9}


@patch(
    "app.modules.ahorro.presentation.controller."
    "ahorro_controller.EliminarAhorroUseCase"
)
def test_eliminar_ahorro_commitea(mock_use_case):

    repository = Mock()
    unit_of_work = Mock()
    controller = AhorroController(repository, unit_of_work)
    current_user = Mock(id_usuario=7)
    mock_use_case.return_value.execute.return_value = {"mensaje": "ok"}

    resultado = controller.eliminar_ahorro(4, current_user)

    mock_use_case.assert_called_once_with(repository, unit_of_work.cuentas)
    mock_use_case.return_value.execute.assert_called_once_with(4, 7)
    unit_of_work.commit.assert_called_once()
    assert resultado == {"mensaje": "ok"}


@patch(
    "app.modules.ahorro.presentation.controller."
    "ahorro_controller.ObtenerProgresoMeta"
)
def test_obtener_progreso_meta_no_commitea(mock_use_case):

    repository = Mock()
    unit_of_work = Mock()
    controller = AhorroController(repository, unit_of_work)
    current_user = Mock(id_usuario=7)
    mock_use_case.return_value.execute.return_value = {"porcentaje": 45.5}

    resultado = controller.obtener_progreso_meta(3, current_user)

    mock_use_case.assert_called_once_with(repository, unit_of_work.cuentas)
    mock_use_case.return_value.execute.assert_called_once_with(3, 7)
    unit_of_work.commit.assert_not_called()
    assert resultado == {"porcentaje": 45.5}
