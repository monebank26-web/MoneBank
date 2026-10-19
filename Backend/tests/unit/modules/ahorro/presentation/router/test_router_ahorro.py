from unittest.mock import Mock, patch

from app.modules.ahorro.presentation.router.router import crear_meta


@patch(
    "app.modules.ahorro.presentation.router.router."
    "RegistrarAbonoAhorro"
)
@patch(
    "app.modules.ahorro.presentation.router.router.CrearMeta"
)
def test_crear_meta_usa_uow_y_commitea(mock_use_case, mock_abono):
    unit_of_work = Mock()
    current_user = Mock(id_usuario=7)
    meta = Mock()
    meta.model_dump.return_value = {"nombre": "Viaje"}
    mock_use_case.return_value.execute.return_value = {"id_ahorro": 1}

    resultado = crear_meta(meta, current_user, unit_of_work)

    mock_abono.assert_called_once_with(unit_of_work.transacciones)
    mock_use_case.assert_called_once_with(
        unit_of_work.ahorros,
        unit_of_work.cuentas,
        mock_abono.return_value,
    )
    mock_use_case.return_value.execute.assert_called_once_with(
        {"nombre": "Viaje"},
        7,
    )
    unit_of_work.commit.assert_called_once()
    assert resultado == {"id_ahorro": 1}
