import pytest
from unittest.mock import Mock
from app.modules.usuario.application.use_cases.obtener_usuario_por_id import ObtenerUsuarioPorIdUseCase



def test_obtener_usuario_por_id_exitoso():
    # Arrange
    mock_repository = Mock()
    mock_db = Mock()

    usuario = {
        "id_usuario": 1,
        "nombres": "David",
        "correo": "david@test.com"
    }

    mock_repository.get_by_id.return_value = usuario

    use_case = ObtenerUsuarioPorIdUseCase(mock_repository)

    # Act
    resultado = use_case.execute(mock_db, 1)

    # Assert
    assert resultado == usuario
    mock_repository.get_by_id.assert_called_once_with(mock_db, 1)

def test_obtener_usuario_por_id_no_existe():
    # Arrange
    mock_repository = Mock()
    mock_db = Mock()

    mock_repository.get_by_id.return_value = None

    use_case = ObtenerUsuarioPorIdUseCase(mock_repository)

    # Act
    resultado = use_case.execute(mock_db, 99)

    # Assert
    assert resultado is None
    mock_repository.get_by_id.assert_called_once_with(mock_db, 99)

def test_obtener_usuario_por_id_none():
    # Arrange
    mock_repository = Mock()
    mock_db = Mock()

    use_case = ObtenerUsuarioPorIdUseCase(mock_repository)

    # Act & Assert
    with pytest.raises(ValueError, match="El id del usuario no puede ser None"):
        use_case.execute(mock_db, None)

    mock_repository.get_by_id.assert_not_called()
