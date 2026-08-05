from unittest.mock import Mock

from app.modules.usuario.application.use_cases.crear_usuario import CrearUsuario


def test_crear_usuario_exitosamente():
    # Arrange
    repository = Mock()
    db = Mock()

    usuario_data = {
        "correo": "usuario@test.com",
        "contraseña": "123456"
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


def test_crear_cuenta_vinculada_usuario():
    # Arrange
    repository = Mock()
    db = Mock()

    usuario_mock = Mock()
    usuario_mock.id_usuario = 1

    repository.create.return_value = usuario_mock

    use_case = CrearUsuario(repository)

    usuario_data = {
        "correo": "usuario@test.com",
        "contraseña": "123456"
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