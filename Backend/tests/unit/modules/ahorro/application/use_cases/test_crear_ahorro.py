from unittest.mock import Mock

from app.modules.ahorro.application.use_cases.crear_ahorro import CrearAhorro


def test_debe_crear_un_ahorro():

    # Arrange
    repository = Mock()

    ahorro_data = {
        "nombre": "Viaje",
        "meta": 500000
    }

    ahorro_creado = {
        "id": 1,
        "nombre": "Viaje",
        "meta": 500000
    }

    repository.create.return_value = ahorro_creado

    use_case = CrearAhorro(repository)

    # Act
    resultado = use_case.execute(ahorro_data)

    # Assert
    repository.create.assert_called_once_with(ahorro_data)

    assert resultado == ahorro_creado
