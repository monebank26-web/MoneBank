from unittest.mock import Mock, patch

from app.core.security.roles import ROL_ADMIN, ROL_USUARIO
from app.modules.cuenta.presentation.controller.cuenta_controller import (
    CuentaController,
)


def _usuario(id_usuario=7, id_rol=ROL_USUARIO):
    return Mock(id_usuario=id_usuario, id_rol=id_rol)


@patch(
    "app.modules.cuenta.presentation.controller."
    "cuenta_controller.ObtenerCuentaPorUsuarioUseCase"
)
@patch(
    "app.modules.cuenta.presentation.controller."
    "cuenta_controller.ObtenerCuentasUseCase"
)
def test_obtener_cuentas_usuario_estandar_solo_ve_las_suyas(
    mock_todas, mock_por_usuario
):

    repository = Mock()
    controller = CuentaController(repository)
    mock_por_usuario.return_value.execute.return_value = {"id_cuenta": 1}

    resultado = controller.obtener_cuentas(_usuario(id_usuario=7))

    mock_por_usuario.assert_called_once_with(repository)
    mock_por_usuario.return_value.execute.assert_called_once_with(7)
    mock_todas.assert_not_called()
    assert resultado == [{"id_cuenta": 1}]


@patch(
    "app.modules.cuenta.presentation.controller."
    "cuenta_controller.ObtenerCuentasUseCase"
)
@patch(
    "app.modules.cuenta.presentation.controller."
    "cuenta_controller.ObtenerCuentaPorUsuarioUseCase"
)
def test_obtener_cuentas_admin_sin_filtro_ve_todas(
    mock_por_usuario, mock_todas
):

    repository = Mock()
    controller = CuentaController(repository)
    mock_todas.return_value.execute.return_value = [{"id_cuenta": 1}]

    resultado = controller.obtener_cuentas(
        _usuario(id_rol=ROL_ADMIN)
    )

    mock_todas.assert_called_once_with(repository)
    mock_todas.return_value.execute.assert_called_once_with()
    mock_por_usuario.assert_not_called()
    assert resultado == [{"id_cuenta": 1}]


@patch(
    "app.modules.cuenta.presentation.controller."
    "cuenta_controller.ObtenerCuentasUseCase"
)
@patch(
    "app.modules.cuenta.presentation.controller."
    "cuenta_controller.ObtenerCuentaPorUsuarioUseCase"
)
def test_obtener_cuentas_admin_con_filtro_ve_cuenta_del_usuario(
    mock_por_usuario, mock_todas
):

    repository = Mock()
    controller = CuentaController(repository)
    mock_por_usuario.return_value.execute.return_value = {"id_cuenta": 9}

    resultado = controller.obtener_cuentas(
        _usuario(id_rol=ROL_ADMIN), usuario_id=42
    )

    mock_por_usuario.assert_called_once_with(repository)
    mock_por_usuario.return_value.execute.assert_called_once_with(42)
    mock_todas.assert_not_called()
    assert resultado == [{"id_cuenta": 9}]


@patch(
    "app.modules.cuenta.presentation.controller."
    "cuenta_controller.ObtenerCuentaPorIdUseCase"
)
def test_obtener_cuenta_por_id_pasa_autorizacion_al_use_case(mock_use_case):

    repository = Mock()
    controller = CuentaController(repository)
    mock_use_case.return_value.execute.return_value = {"id_cuenta": 1}

    controller.obtener_cuenta_por_id(1, _usuario(id_usuario=7))
    mock_use_case.return_value.execute.assert_called_with(1, 7, False)

    controller.obtener_cuenta_por_id(
        1, _usuario(id_usuario=7, id_rol=ROL_ADMIN)
    )
    mock_use_case.return_value.execute.assert_called_with(1, 7, True)


@patch(
    "app.modules.cuenta.presentation.controller."
    "cuenta_controller.ActualizarCuentaUseCase"
)
def test_actualizar_cuenta_pasa_autorizacion_al_use_case(mock_use_case):

    from app.modules.cuenta.presentation.schema.cuenta_schema import CuentaUpdate

    repository = Mock()
    controller = CuentaController(repository)
    mock_use_case.return_value.execute.return_value = {"id_cuenta": 1}

    cuenta = CuentaUpdate(estado="INACTIVA")

    controller.actualizar_cuenta(1, cuenta, _usuario(id_usuario=7))

    mock_use_case.assert_called_once_with(repository)
    mock_use_case.return_value.execute.assert_called_once_with(
        1, cuenta.model_dump(exclude_unset=True), 7, False
    )


@patch(
    "app.modules.cuenta.presentation.controller."
    "cuenta_controller.EliminarCuentaUseCase"
)
def test_eliminar_cuenta_pasa_autorizacion_al_use_case(mock_use_case):

    repository = Mock()
    controller = CuentaController(repository)
    mock_use_case.return_value.execute.return_value = {"mensaje": "ok"}

    resultado = controller.eliminar_cuenta(1, _usuario(id_usuario=7))

    mock_use_case.assert_called_once_with(repository)
    mock_use_case.return_value.execute.assert_called_once_with(1, 7, False)
    assert resultado == {"mensaje": "ok"}
