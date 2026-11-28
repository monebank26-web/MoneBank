from datetime import datetime, timedelta, timezone
from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from app.modules.auth.application.use_cases.codigo_recuperacion import (
    hash_codigo_recuperacion,
)
from app.modules.auth.application.use_cases.confirm_password_recovery import (
    ConfirmPasswordRecoveryUseCase,
)
from app.modules.auth.domain.entity.reset_token import ResetToken
from app.shared.exceptions.auth_errors import (
    ContrasenaInvalidaException,
    InvalidOrExpiredTokenException,
)


def crear_usuario():
    return SimpleNamespace(
        id_usuario=1,
        correo="usuario@test.com",
    )


def crear_token_valido():
    return ResetToken(
        id=1,
        usuario_id=1,
        token_hash=hash_codigo_recuperacion(1, "123456"),
        fecha_expiracion=datetime.now(timezone.utc) + timedelta(minutes=15),
        usado=False,
    )


def crear_token_expirado():
    return ResetToken(
        id=1,
        usuario_id=1,
        token_hash=hash_codigo_recuperacion(1, "123456"),
        fecha_expiracion=datetime.now(timezone.utc) - timedelta(minutes=5),
        usado=False,
    )


def crear_token_ya_usado():
    return ResetToken(
        id=1,
        usuario_id=1,
        token_hash=hash_codigo_recuperacion(1, "123456"),
        fecha_expiracion=datetime.now(timezone.utc) + timedelta(minutes=15),
        usado=True,
    )


def crear_repositorios():
    auth_repository = Mock()
    usuario_repository = Mock()
    usuario_repository.get_by_email_recuperacion.return_value = crear_usuario()
    auth_repository.find_active_recovery_token.return_value = None
    return auth_repository, usuario_repository


def test_confirmar_recuperacion_exitosa():
    auth_repository, usuario_repository = crear_repositorios()
    auth_repository.find_valid_token.return_value = crear_token_valido()

    use_case = ConfirmPasswordRecoveryUseCase(
        auth_repository,
        usuario_repository,
    )

    resultado = use_case.execute(
        "usuario@test.com",
        "123456",
        "MiClave1!",
    )

    assert resultado["mensaje"] == "Contraseña restablecida exitosamente"

    usuario_repository.get_by_email_recuperacion.assert_called_once_with(
        "usuario@test.com"
    )
    auth_repository.find_valid_token.assert_called_once_with(
        1,
        hash_codigo_recuperacion(1, "123456"),
    )
    usuario_repository.update_password.assert_called_once()
    usuario_repository.update_auth_fields.assert_called_once_with(1, 0, None)
    auth_repository.invalidate_token.assert_called_once_with(1)


def test_confirmar_recuperacion_correo_no_existe():
    auth_repository, usuario_repository = crear_repositorios()
    usuario_repository.get_by_email_recuperacion.return_value = None

    use_case = ConfirmPasswordRecoveryUseCase(
        auth_repository,
        usuario_repository,
    )

    with pytest.raises(InvalidOrExpiredTokenException):
        use_case.execute("no@existe.com", "123456", "MiClave1!")

    auth_repository.find_valid_token.assert_not_called()
    usuario_repository.update_password.assert_not_called()
    usuario_repository.update_auth_fields.assert_not_called()
    auth_repository.invalidate_token.assert_not_called()


def test_confirmar_recuperacion_codigo_no_existe():
    auth_repository, usuario_repository = crear_repositorios()
    auth_repository.find_valid_token.return_value = None

    use_case = ConfirmPasswordRecoveryUseCase(
        auth_repository,
        usuario_repository,
    )

    with pytest.raises(InvalidOrExpiredTokenException):
        use_case.execute("usuario@test.com", "000000", "MiClave1!")

    auth_repository.find_active_recovery_token.assert_called_once_with(1)
    auth_repository.update_recovery_token_attempts.assert_not_called()
    usuario_repository.update_password.assert_not_called()
    usuario_repository.update_auth_fields.assert_not_called()
    auth_repository.invalidate_token.assert_not_called()


def test_confirmar_recuperacion_codigo_expirado():
    auth_repository, usuario_repository = crear_repositorios()
    auth_repository.find_valid_token.return_value = crear_token_expirado()

    use_case = ConfirmPasswordRecoveryUseCase(
        auth_repository,
        usuario_repository,
    )

    with pytest.raises(InvalidOrExpiredTokenException):
        use_case.execute("usuario@test.com", "123456", "MiClave1!")

    auth_repository.find_active_recovery_token.assert_called_once_with(1)
    auth_repository.update_recovery_token_attempts.assert_not_called()
    usuario_repository.update_password.assert_not_called()
    usuario_repository.update_auth_fields.assert_not_called()
    auth_repository.invalidate_token.assert_not_called()


def test_confirmar_recuperacion_codigo_ya_usado():
    auth_repository, usuario_repository = crear_repositorios()
    auth_repository.find_valid_token.return_value = crear_token_ya_usado()

    use_case = ConfirmPasswordRecoveryUseCase(
        auth_repository,
        usuario_repository,
    )

    with pytest.raises(InvalidOrExpiredTokenException):
        use_case.execute("usuario@test.com", "123456", "MiClave1!")

    auth_repository.find_active_recovery_token.assert_called_once_with(1)
    auth_repository.update_recovery_token_attempts.assert_not_called()
    usuario_repository.update_password.assert_not_called()
    usuario_repository.update_auth_fields.assert_not_called()
    auth_repository.invalidate_token.assert_not_called()


def test_codigo_incorrecto_incrementa_los_intentos_del_codigo_activo():
    auth_repository, usuario_repository = crear_repositorios()
    auth_repository.find_valid_token.return_value = None
    auth_repository.find_active_recovery_token.return_value = SimpleNamespace(
        id=7,
        intentos_fallidos=2,
    )

    use_case = ConfirmPasswordRecoveryUseCase(
        auth_repository,
        usuario_repository,
    )

    with pytest.raises(InvalidOrExpiredTokenException):
        use_case.execute("usuario@test.com", "000000", "MiClave1!")

    auth_repository.update_recovery_token_attempts.assert_called_once_with(
        7,
        3,
        False,
    )


def test_codigo_incorrecto_marca_el_codigo_usado_al_llegar_al_maximo():
    auth_repository, usuario_repository = crear_repositorios()
    auth_repository.find_valid_token.return_value = None
    auth_repository.find_active_recovery_token.return_value = SimpleNamespace(
        id=7,
        intentos_fallidos=4,
    )

    use_case = ConfirmPasswordRecoveryUseCase(
        auth_repository,
        usuario_repository,
    )

    with pytest.raises(InvalidOrExpiredTokenException):
        use_case.execute("usuario@test.com", "000000", "MiClave1!")

    auth_repository.update_recovery_token_attempts.assert_called_once_with(
        7,
        5,
        True,
    )


def test_contrasena_debil_no_consume_el_codigo():
    auth_repository, usuario_repository = crear_repositorios()
    auth_repository.find_valid_token.return_value = crear_token_valido()

    use_case = ConfirmPasswordRecoveryUseCase(
        auth_repository,
        usuario_repository,
    )

    with pytest.raises(ContrasenaInvalidaException):
        use_case.execute("usuario@test.com", "123456", "123")

    auth_repository.find_active_recovery_token.assert_not_called()
    auth_repository.update_recovery_token_attempts.assert_not_called()
    usuario_repository.update_password.assert_not_called()
    usuario_repository.update_auth_fields.assert_not_called()
    auth_repository.invalidate_token.assert_not_called()


def test_confirmar_recuperacion_reinicia_intentos_sin_tocar_el_estado():
    auth_repository, _ = crear_repositorios()
    auth_repository.find_valid_token.return_value = crear_token_valido()
    usuario = SimpleNamespace(
        id_usuario=1,
        correo="usuario@test.com",
        contrasena="hash-viejo",
        estado="BLOQUEADO",
        motivo_bloqueo="Fraude",
        fecha_bloqueo="2026-01-02 10:30:00",
        intentos_fallidos=5,
        bloqueado_hasta="2026-01-02 11:00:00",
    )

    class UsuarioRepositoryFake:
        def get_by_email_recuperacion(self, correo):
            if usuario.correo == correo:
                return usuario
            return None

        def update_password(self, id_usuario, nuevo_hash):
            usuario.contrasena = nuevo_hash

        def update_auth_fields(self, id_usuario, intentos, bloqueado_hasta):
            usuario.intentos_fallidos = intentos
            usuario.bloqueado_hasta = bloqueado_hasta

    use_case = ConfirmPasswordRecoveryUseCase(
        auth_repository,
        UsuarioRepositoryFake(),
    )

    use_case.execute("usuario@test.com", "123456", "ClaveNueva1!")

    assert usuario.intentos_fallidos == 0
    assert usuario.bloqueado_hasta is None
    assert usuario.estado == "BLOQUEADO"
    assert usuario.motivo_bloqueo == "Fraude"
    assert usuario.fecha_bloqueo == "2026-01-02 10:30:00"
