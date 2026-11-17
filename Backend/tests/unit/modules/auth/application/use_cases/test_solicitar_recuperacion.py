from types import SimpleNamespace
from unittest.mock import Mock, patch

from app.modules.auth.application.use_cases.request_password_recovery import (
    MENSAJE_SOLICITUD_RECUPERACION,
    RequestPasswordRecoveryUseCase,
)


def crear_usuario_mock():
    return SimpleNamespace(
        id_usuario=1,
        correo="usuario@test.com"
    )


class AuthRepositoryFake:

    def __init__(self):
        self.invalidaciones = []
        self.creaciones = []

    def find_latest_recovery_token(self, usuario_id):
        return None

    def invalidate_user_tokens(self, usuario_id):
        self.invalidaciones.append(usuario_id)

    def exists_recovery_token_hash(self, token_hash):
        return False

    def create_recovery_token(self, usuario_id, token_hash, fecha_expiracion,
                              intentos_fallidos=0):
        self.creaciones.append(
            (usuario_id, token_hash, fecha_expiracion, intentos_fallidos)
        )


def test_solicitar_recuperacion_exitosa():
    auth_repository = Mock()
    usuario_repository = Mock()
    email_service = Mock()
    usuario_repository.get_by_email_recuperacion.return_value = (
        crear_usuario_mock()
    )
    email_service.send_recovery_email.return_value = True

    use_case = RequestPasswordRecoveryUseCase(
        auth_repository, usuario_repository, email_service
    )

    with patch(
        "app.modules.auth.application.use_cases.request_password_recovery."
        "crear_codigo_recuperacion",
        return_value="123456",
    ):
        resultado = use_case.execute("usuario@test.com")

    assert resultado["mensaje"] == MENSAJE_SOLICITUD_RECUPERACION
    assert resultado["_correo_enviado"] is True

    usuario_repository.get_by_email_recuperacion.assert_called_once_with(
        "usuario@test.com"
    )
    email_service.send_recovery_email.assert_called_once_with(
        "usuario@test.com",
        "123456",
    )


def test_solicitar_recuperacion_correo_no_existe():
    auth_repository = Mock()
    usuario_repository = Mock()
    email_service = Mock()
    usuario_repository.get_by_email_recuperacion.return_value = None

    use_case = RequestPasswordRecoveryUseCase(
        auth_repository, usuario_repository, email_service
    )

    resultado = use_case.execute("no@existe.com")

    assert resultado["mensaje"] == MENSAJE_SOLICITUD_RECUPERACION
    assert resultado["_correo_enviado"] is True
    auth_repository.invalidate_user_tokens.assert_not_called()
    auth_repository.create_recovery_token.assert_not_called()
    email_service.send_recovery_email.assert_not_called()


def test_solicitar_recuperacion_invalida_codigos_viejos():
    auth_repository = AuthRepositoryFake()
    usuario_repository = Mock()
    email_service = Mock()
    email_service.send_recovery_email.return_value = True
    usuario_repository.get_by_email_recuperacion.return_value = (
        crear_usuario_mock()
    )

    use_case = RequestPasswordRecoveryUseCase(
        auth_repository, usuario_repository, email_service
    )

    use_case.execute("usuario@test.com")

    assert auth_repository.invalidaciones == [1]
    assert len(auth_repository.creaciones) == 1
    assert auth_repository.creaciones[0][0] == 1
    assert auth_repository.creaciones[0][3] == 0


def test_solicitar_recuperacion_envia_codigo_por_correo():
    auth_repository = Mock()
    usuario_repository = Mock()
    email_service = Mock()
    email_service.send_recovery_email.return_value = True
    usuario_repository.get_by_email_recuperacion.return_value = (
        crear_usuario_mock()
    )

    use_case = RequestPasswordRecoveryUseCase(
        auth_repository, usuario_repository, email_service
    )

    with patch(
        "app.modules.auth.application.use_cases.request_password_recovery."
        "crear_codigo_recuperacion",
        return_value="000042",
    ):
        use_case.execute("  USUARIO@test.com ")

    email_service.send_recovery_email.assert_called_once_with(
        "usuario@test.com",
        "000042",
    )


def test_solicitar_recuperacion_en_enfriamiento_responde_generico_y_no_envia():
    auth_repository = Mock()
    usuario_repository = Mock()
    email_service = Mock()
    usuario_repository.get_by_email_recuperacion.return_value = (
        crear_usuario_mock()
    )

    use_case = RequestPasswordRecoveryUseCase(
        auth_repository, usuario_repository, email_service
    )

    with patch(
        "app.modules.auth.application.use_cases.request_password_recovery."
        "crear_codigo_recuperacion",
        return_value=None,
    ):
        resultado = use_case.execute("usuario@test.com")

    assert resultado["mensaje"] == MENSAJE_SOLICITUD_RECUPERACION
    assert resultado["_correo_enviado"] is True
    email_service.send_recovery_email.assert_not_called()


def test_solicitar_recuperacion_con_fallo_de_correo_mantiene_respuesta_generica():
    auth_repository = Mock()
    usuario_repository = Mock()
    email_service = Mock()
    email_service.send_recovery_email.return_value = False
    usuario_repository.get_by_email_recuperacion.return_value = (
        crear_usuario_mock()
    )

    use_case = RequestPasswordRecoveryUseCase(
        auth_repository, usuario_repository, email_service
    )

    with patch(
        "app.modules.auth.application.use_cases.request_password_recovery."
        "crear_codigo_recuperacion",
        return_value="123456",
    ):
        resultado = use_case.execute("usuario@test.com")

    assert resultado["mensaje"] == MENSAJE_SOLICITUD_RECUPERACION
    assert resultado["_correo_enviado"] is False
