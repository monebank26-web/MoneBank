from unittest.mock import Mock

import pytest

from app.core.security.PasswordHasher import PasswordHasher
from app.core.security.roles import ROL_USUARIO
from app.modules.usuario.application.use_cases.crear_usuario import CrearUsuario
from app.shared.exceptions.business_exceptions import EmailAlreadyExistsException


def test_crear_usuario_exitosamente():
    # Arrange
    repository = Mock()
    repository.exists_by_email.return_value = False
    cuenta_repository = Mock()

    usuario_data = {
        "correo": "usuario@test.com",
        "contrasena": "123456"
    }

    usuario_mock = Mock()
    usuario_mock.id_usuario = 1

    repository.create.return_value = usuario_mock

    use_case = CrearUsuario(repository, cuenta_repository)

    # Act
    resultado = use_case.execute(usuario_data)

    # Assert
    assert resultado == usuario_mock

    repository.exists_by_email.assert_called_once_with("usuario@test.com")
    repository.create.assert_called_once_with(usuario_data)


def test_crear_usuario_hashea_contrasena_y_aplica_defaults():
    # Arrange
    repository = Mock()
    repository.exists_by_email.return_value = False
    cuenta_repository = Mock()

    usuario_data = {
        "correo": "usuario@test.com",
        "contrasena": "123456"
    }

    repository.create.return_value = Mock(id_usuario=1)

    use_case = CrearUsuario(repository, cuenta_repository)

    # Act
    use_case.execute(usuario_data)

    # Assert
    assert usuario_data["contrasena"] != "123456"
    assert PasswordHasher.verify("123456", usuario_data["contrasena"])

    assert usuario_data["estado"] == "ACTIVO"
    assert usuario_data["id_rol"] == ROL_USUARIO
    assert usuario_data["id_tipo_usuario"] == 3


def test_crear_cuenta_vinculada_usuario():
    # Arrange
    repository = Mock()
    repository.exists_by_email.return_value = False
    cuenta_repository = Mock()

    usuario_mock = Mock()
    usuario_mock.id_usuario = 1

    repository.create.return_value = usuario_mock

    use_case = CrearUsuario(repository, cuenta_repository)

    usuario_data = {
        "correo": "usuario@test.com",
        "contrasena": "123456"
    }

    # Act
    use_case.execute(usuario_data)

    # Assert
    cuenta_repository.create.assert_called_once_with({
        "saldo": 0,
        "estado": "ACTIVA",
        "id_usuario": 1,
    })


def test_crear_usuario_correo_duplicado_rechaza():
    # Arrange
    repository = Mock()
    repository.exists_by_email.return_value = True
    cuenta_repository = Mock()

    use_case = CrearUsuario(repository, cuenta_repository)

    usuario_data = {
        "correo": "usuario@test.com",
        "contrasena": "123456"
    }

    # Act & Assert
    with pytest.raises(EmailAlreadyExistsException):
        use_case.execute(usuario_data)

    repository.create.assert_not_called()
    cuenta_repository.create.assert_not_called()
