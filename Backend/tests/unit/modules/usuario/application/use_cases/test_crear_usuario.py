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
    db = Mock()

    usuario_data = {
        "correo": "usuario@test.com",
        "contrasena": "123456"
    }

    usuario_mock = Mock()
    usuario_mock.id_usuario = 1

    repository.create.return_value = usuario_mock

    use_case = CrearUsuario(repository)

    # Act
    resultado = use_case.execute(
        db,
        usuario_data
    )

    # Assert
    assert resultado == usuario_mock

    repository.create.assert_called_once_with(
        db,
        usuario_data
    )


def test_crear_usuario_hashea_contrasena_y_aplica_defaults():
    # Arrange
    repository = Mock()
    repository.exists_by_email.return_value = False
    db = Mock()

    usuario_data = {
        "correo": "usuario@test.com",
        "contrasena": "123456"
    }

    repository.create.return_value = Mock(id_usuario=1)

    use_case = CrearUsuario(repository)

    # Act
    use_case.execute(
        db,
        usuario_data
    )

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
    db = Mock()

    usuario_mock = Mock()
    usuario_mock.id_usuario = 1

    repository.create.return_value = usuario_mock

    use_case = CrearUsuario(repository)

    usuario_data = {
        "correo": "usuario@test.com",
        "contrasena": "123456"
    }

    # Act
    use_case.execute(
        db,
        usuario_data
    )

    # Assert
    db.add.assert_called_once()

    cuenta_creada = db.add.call_args.args[0]

    assert cuenta_creada.saldo == 0
    assert cuenta_creada.estado == "ACTIVA"
    assert cuenta_creada.id_usuario == 1

    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(cuenta_creada)


def test_crear_usuario_correo_duplicado_rechaza():
    # Arrange
    repository = Mock()
    repository.exists_by_email.return_value = True
    db = Mock()

    use_case = CrearUsuario(repository)

    usuario_data = {
        "correo": "usuario@test.com",
        "contrasena": "123456"
    }

    # Act & Assert
    with pytest.raises(EmailAlreadyExistsException):
        use_case.execute(
            db,
            usuario_data
        )

    repository.create.assert_not_called()
