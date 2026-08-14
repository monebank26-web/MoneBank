from unittest.mock import Mock

from app.modules.cuenta.application.use_cases.obtener_cuenta import ObtenerCuentasUseCase


def test_obtener_cuentas_exitosamente():

    # Arrange
    repository = Mock()
    db = Mock()

    cuentas_mock = [
        {
            "id_cuenta": 1,
            "saldo": 10000,
            "estado": "ACTIVA"
        }
    ]

    repository.get_all.return_value = cuentas_mock

    use_case = ObtenerCuentasUseCase(repository)

    # Act
    resultado = use_case.execute(db)

    # Assert
    assert resultado == cuentas_mock

    repository.get_all.assert_called_once_with(db)