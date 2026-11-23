from unittest.mock import Mock
from app.modules.usuario.application.use_cases.obtener_usuario_por_id import ObtenerUsuarioPorIdUseCase



def test_obtener_usuario_por_id_exitoso():
    # Arrange
    mock_repository = Mock()

    usuario = {
        "id_usuario": 1,
        "nombres": "David",
        "correo": "david@test.com"
    }

    mock_repository.get_by_id.return_value = usuario

    use_case = ObtenerUsuarioPorIdUseCase(mock_repository)

    # Act
    resultado = use_case.execute(1)

    # Assert
    assert resultado == usuario
    mock_repository.get_by_id.assert_called_once_with(1)

def test_obtener_usuario_por_id_no_existe():
    # Arrange
    mock_repository = Mock()

    mock_repository.get_by_id.return_value = None

    use_case = ObtenerUsuarioPorIdUseCase(mock_repository)

    # Act
    resultado = use_case.execute(99)

    # Assert
    assert resultado is None
    mock_repository.get_by_id.assert_called_once_with(99)
