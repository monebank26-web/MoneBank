from unittest.mock import Mock

import pytest

from app.modules.cuenta.application.use_cases.crear_cuenta import CrearCuenta
from app.shared.exceptions.business_exceptions import EstadoInvalido


def test_crear_cuenta_exitosamente():

    # Arrange
    repository = Mock()

    cuenta_data = {
        "saldo": 0,
        "estado": "ACTIVA",
        "id_usuario": 1
    }

    cuenta_mock = Mock()

    repository.create.return_value = cuenta_mock

    use_case = CrearCuenta(repository)

    # Act
    resultado = use_case.execute(cuenta_data)

    # Assert
    assert resultado == cuenta_mock

    repository.create.assert_called_once_with(cuenta_data)


def test_estado_invalido_lanza_estado_invalido():

    repository = Mock()

    cuenta_data = {
        "saldo": 0,
        "estado": "BLOQUEADA",
        "id_usuario": 1
    }

    with pytest.raises(EstadoInvalido):
        CrearCuenta(repository).execute(cuenta_data)

    repository.create.assert_not_called()