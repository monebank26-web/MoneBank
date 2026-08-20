from unittest.mock import Mock

from app.modules.cuenta.application.use_cases.obtener_cuenta_por_id import (
    ObtenerCuentaPorIdUseCase
)


def test_debe_obtener_cuenta_por_id():

    repository = Mock()

    cuenta = {
        "id_cuenta": 1,
        "saldo": 150000,
        "id_usuario": 3
    }

    repository.get_by_id.return_value = cuenta

    use_case = ObtenerCuentaPorIdUseCase(repository)

    resultado = use_case.execute(3)

    repository.get_by_id.assert_called_once_with(3)

    assert resultado["success"] is True
    assert resultado["cuenta"] == cuenta
