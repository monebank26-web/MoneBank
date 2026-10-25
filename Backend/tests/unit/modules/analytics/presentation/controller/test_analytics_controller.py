from decimal import Decimal
from unittest.mock import Mock, patch

from app.modules.analytics.presentation.controller.analytics_controller import (
    CONSEJO_GENERICO,
    AnalyticsController,
)
from app.modules.analytics.presentation.schema.consejo_previo_schema import (
    ConsejoPrevioRequest,
)
from app.shared.exceptions.chat_ia_errors import ConsejoIANoDisponible


def crear_controller():
    return AnalyticsController(Mock(), Mock(), Mock())


@patch(
    "app.modules.analytics.presentation.controller."
    "analytics_controller.ObtenerConsejoIA"
)
def test_obtener_consejo_ia_exitoso_generado_con_ia_true(mock_use_case):

    controller = crear_controller()
    current_user = Mock(id_usuario=7)
    mock_use_case.return_value.execute.return_value = "Ahorra más esta semana."

    resultado = controller.obtener_consejo_ia(4, current_user)

    mock_use_case.return_value.execute.assert_called_once_with(7, 4)
    assert resultado.consejo == "Ahorra más esta semana."
    assert resultado.generado_con_ia is True


@patch(
    "app.modules.analytics.presentation.controller."
    "analytics_controller.ObtenerConsejoIA"
)
def test_obtener_consejo_ia_sin_ia_usa_consejo_generico(mock_use_case):

    controller = crear_controller()
    current_user = Mock(id_usuario=7)
    mock_use_case.return_value.execute.side_effect = ConsejoIANoDisponible()

    resultado = controller.obtener_consejo_ia(4, current_user)

    assert resultado.consejo == CONSEJO_GENERICO
    assert resultado.generado_con_ia is False


@patch(
    "app.modules.analytics.presentation.controller."
    "analytics_controller.ObtenerConsejoPrevio"
)
def test_obtener_consejo_previo_sin_ia_usa_consejo_generico(mock_use_case):

    controller = crear_controller()
    current_user = Mock(id_usuario=7)
    mock_use_case.return_value.execute.side_effect = ConsejoIANoDisponible()
    request = ConsejoPrevioRequest(monto=Decimal("1500"), id_categoria=2)

    resultado = controller.obtener_consejo_previo(request, current_user)

    mock_use_case.return_value.execute.assert_called_once_with(
        7,
        Decimal("1500"),
        2,
    )
    assert resultado.consejo == CONSEJO_GENERICO
    assert resultado.generado_con_ia is False


@patch(
    "app.modules.analytics.presentation.controller."
    "analytics_controller.ObtenerGraficas"
)
def test_obtener_graficas_no_commitea(mock_use_case):

    controller = crear_controller()
    current_user = Mock(id_usuario=7)
    mock_use_case.return_value.execute.return_value = {"periodo": "mensual"}

    resultado = controller.obtener_graficas(current_user, "mensual")

    mock_use_case.assert_called_once_with(controller.repository)
    mock_use_case.return_value.execute.assert_called_once_with(7, "mensual")
    controller.unit_of_work.commit.assert_not_called()
    assert resultado == {"periodo": "mensual"}


@patch(
    "app.modules.analytics.presentation.controller."
    "analytics_controller.GenerarReporte"
)
def test_generar_reporte_no_commitea(mock_use_case):

    controller = crear_controller()
    current_user = Mock(id_usuario=7)
    mock_use_case.return_value.execute.return_value = {"periodo_inicio": "2026-09"}

    resultado = controller.generar_reporte(current_user, "mensual", None, None)

    mock_use_case.assert_called_once_with(controller.repository)
    mock_use_case.return_value.execute.assert_called_once_with(
        7,
        "mensual",
        None,
        None,
    )
    controller.unit_of_work.commit.assert_not_called()
    assert resultado == {"periodo_inicio": "2026-09"}
