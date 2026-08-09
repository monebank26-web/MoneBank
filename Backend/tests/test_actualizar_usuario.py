from unittest.mock import MagicMock
import pytest

from app.modules.usuario.application.use_cases.actualizar_usuarios import ActualizarUsuarioUseCase


def test_execute_actualiza_usuario():
    # Arrange
    repository = MagicMock()
    use_case = ActualizarUsuarioUseCase(repository)

    db = MagicMock()
    id_usuario = 1
    usuario_data = {
        "nombre": "Juan",
        "correo": "juan@gmail.com"
    }

    resultado_esperado = {
        "id": 1,
        "nombre": "Juan",
        "correo": "juan@gmail.com"
    }

    repository.update.return_value = resultado_esperado

    # Act
    resultado = use_case.execute(db, id_usuario, usuario_data)

    # Assert
    repository.update.assert_called_once_with(
        db,
        id_usuario,
        usuario_data
    )
    assert resultado == resultado_esperado


def test_execute_lanza_excepcion():
    # Arrange
    repository = MagicMock()
    use_case = ActualizarUsuarioUseCase(repository)

    repository.update.side_effect = Exception("Error al actualizar")

    # Act & Assert
    with pytest.raises(Exception, match="Error al actualizar"):
        use_case.execute(
            MagicMock(),
            1,
            {"nombre": "Juan"}
        )