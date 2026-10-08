from datetime import datetime
from unittest.mock import Mock, patch

from app.modules.transaccion.presentation.controller.transaccion_controller import (
    TransaccionController,
)
from app.modules.transaccion.presentation.schema.trans_schema import (
    GastoRequest,
    HistorialRequest,
    TransaccionUpdateRequest,
)


@patch(
    "app.modules.transaccion.presentation.controller."
    "transaccion_controller.RegistrarGasto"
)
def test_registrar_gasto_ejecuta_use_case(mock_use_case):

    repository = Mock()
    controller = TransaccionController(repository)
    current_user = Mock(id_usuario=7)

    gasto = GastoRequest(
        monto=15000,
        fecha=datetime(2026, 10, 1, 10, 0, 0),
        id_cuenta=2,
        id_categoria=5,
    )

    mock_use_case.return_value.execute.return_value = {"id_transaccion": 1}

    resultado = controller.registrar_gasto(gasto, current_user)

    mock_use_case.assert_called_once_with(repository)
    mock_use_case.return_value.execute.assert_called_once_with(
        gasto.model_dump(), 7
    )
    assert resultado == {"id_transaccion": 1}


@patch(
    "app.modules.transaccion.presentation.controller."
    "transaccion_controller.ObtenerHistorialUseCase"
)
def test_obtener_historial_ejecuta_use_case(mock_use_case):

    repository = Mock()
    controller = TransaccionController(repository)
    current_user = Mock(id_usuario=7)

    filtros = HistorialRequest()

    mock_use_case.return_value.execute.return_value = {"items": []}

    resultado = controller.obtener_historial(current_user, filtros)

    mock_use_case.assert_called_once_with(repository)
    mock_use_case.return_value.execute.assert_called_once_with(
        7, filtros.model_dump()
    )
    assert resultado == {"items": []}


@patch(
    "app.modules.transaccion.presentation.controller."
    "transaccion_controller.ObtenerCategoriasUseCase"
)
def test_obtener_categorias_ejecuta_use_case(mock_use_case):

    repository = Mock()
    controller = TransaccionController(repository)
    current_user = Mock(id_usuario=7)

    mock_use_case.return_value.execute.return_value = [{"id_categoria": 1}]

    resultado = controller.obtener_categorias(current_user)

    mock_use_case.assert_called_once_with(repository)
    mock_use_case.return_value.execute.assert_called_once_with()
    assert resultado == [{"id_categoria": 1}]


@patch(
    "app.modules.transaccion.presentation.controller."
    "transaccion_controller.ObtenerDetalleUseCase"
)
def test_obtener_detalle_ejecuta_use_case(mock_use_case):

    repository = Mock()
    controller = TransaccionController(repository)
    current_user = Mock(id_usuario=7)

    mock_use_case.return_value.execute.return_value = {"id_transaccion": 42}

    resultado = controller.obtener_detalle(42, current_user)

    mock_use_case.assert_called_once_with(repository)
    mock_use_case.return_value.execute.assert_called_once_with(7, 42)
    assert resultado == {"id_transaccion": 42}


@patch(
    "app.modules.transaccion.presentation.controller."
    "transaccion_controller.ActualizarTransaccion"
)
def test_actualizar_transaccion_ejecuta_use_case(mock_use_case):

    repository = Mock()
    controller = TransaccionController(repository)
    current_user = Mock(id_usuario=7)

    transaccion = TransaccionUpdateRequest(
        monto=2000,
        id_categoria=5,
    )

    mock_use_case.return_value.execute.return_value = {"id_transaccion": 10}

    resultado = controller.actualizar_transaccion(10, transaccion, current_user)

    mock_use_case.assert_called_once_with(repository)
    mock_use_case.return_value.execute.assert_called_once_with(
        10, transaccion.model_dump(), 7
    )
    assert resultado == {"id_transaccion": 10}
