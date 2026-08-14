from unittest.mock import Mock

from app.modules.cuenta.application.use_cases.crear_cuenta import CrearCuenta


def test_crear_cuenta_exitosamente():

    # Arrange
    repository = Mock()
    db = Mock()

    cuenta_data = {
        "saldo": 0,
        "estado": "ACTIVA",
        "id_usuario": 1
    }

    cuenta_mock = Mock()

    repository.create.return_value = cuenta_mock

    use_case = CrearCuenta(repository)

    # Act
    resultado = use_case.execute(
        db,
        cuenta_data
    )

    # Assert
    assert resultado == cuenta_mock

    repository.create.assert_called_once_with(
        db,
        cuenta_data
    )