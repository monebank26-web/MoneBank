from unittest.mock import Mock

from app.modules.usuario.application.use_cases.login_usuario import LoginUsuarioUseCase


def test_login_exitoso():
    # Arrange
    repository = Mock()

    repository.buscar_por_correo.return_value = {
        "id": 1,
        "correo": "usuario@test.com",
        "contrasena": "123456"
    }

    use_case = LoginUsuarioUseCase(repository)

    # Act
    resultado = use_case.execute(
        None,
        "usuario@test.com",
        "123456"
    )

    # Assert
    assert resultado["success"] is True
    assert resultado["usuario"]["correo"] == "usuario@test.com"


def test_login_usuario_no_existe():
    # Arrange
    repository = Mock()

    repository.buscar_por_correo.return_value = None

    use_case = LoginUsuarioUseCase(repository)

    # Act
    resultado = use_case.execute(
        None,
        "usuario@test.com",
        "123456"
    )

    # Assert
    assert resultado["success"] is False
    assert resultado["message"] == "Credenciales incorrectas"


def test_login_contrasena_incorrecta():
    # Arrange
    repository = Mock()

    repository.buscar_por_correo.return_value = {
        "id": 1,
        "correo": "usuario@test.com",
        "contrasena": "123456"
    }

    use_case = LoginUsuarioUseCase(repository)

    # Act
    resultado = use_case.execute(
        None,
        "usuario@test.com",
        "000000"
    )

    # Assert
    assert resultado["success"] is False
    assert resultado["message"] == "Credenciales incorrectas"