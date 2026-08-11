from unittest.mock import Mock

from app.modules.cuenta.application.use_cases.obtener_cuenta_por_id import (
    ObtenerCuentaPorIdUseCase
)

def test_debe_obtener_cuenta_por_id():

    repository = Mock()
    db = Mock()

    cuenta = {
        "id": 1,
        "saldo": 150000
    }

    repository.get_by_id.return_value = cuenta

    use_case = ObtenerCuentaPorIdUseCase(repository)

    resultado = use_case.execute(db, 1)

    repository.get_by_id.assert_called_once_with(db, 1)

    assert resultado["success"] is True
    assert resultado["cuenta"] == cuenta