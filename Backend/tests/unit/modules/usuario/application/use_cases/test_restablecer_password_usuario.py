from datetime import datetime, timedelta, timezone
from types import SimpleNamespace
from unittest.mock import Mock, patch

import pytest

from app.core.constants import MINUTOS_TOKEN_RECUPERACION
from app.core.security.PasswordHasher import PasswordHasher
from app.core.security.reset_token import TokenGenerator
from app.modules.auth.application.use_cases.confirm_password_recovery import (
    ConfirmPasswordRecoveryUseCase,
)
from app.modules.auth.domain.entity.reset_token import ResetToken
from app.modules.usuario.application.use_cases.restablecer_password_usuario import (
    RestablecerPasswordUsuario,
)
from app.shared.constants.acciones import ACCION_RESTABLECER_PASSWORD
from app.shared.exceptions.common import UsuarioNotFoundException
from app.shared.exceptions.usuario_errors import (
    NoPuedeRestablecerPasswordPropiaException,
)


class AuthRepositoryFake:

    def __init__(self):
        self.tokens = {}
        self._siguiente_id = 1

    def invalidate_user_tokens(self, usuario_id):
        for token in self.tokens.values():
            if token.usuario_id == usuario_id:
                token.usado = True

    def create_recovery_token(self, usuario_id, token_hash, fecha_expiracion):
        token = ResetToken(
            id=self._siguiente_id,
            usuario_id=usuario_id,
            token_hash=token_hash,
            fecha_expiracion=fecha_expiracion,
            usado=False,
        )
        self.tokens[token_hash] = token
        self._siguiente_id += 1
        return token

    def find_valid_token(self, token_hash):
        token = self.tokens.get(token_hash)

        if (
            token
            and not token.esta_expirado()
            and not token.fue_utilizado()
        ):
            return token

        return None

    def invalidate_token(self, token_id):
        for token in self.tokens.values():
            if token.id == token_id:
                token.usado = True


class UsuarioRepositoryFake:

    def __init__(self, usuario):
        self.usuario = usuario

    def get_by_id(self, id_usuario):
        if self.usuario.id_usuario == id_usuario:
            return self.usuario
        return None

    def update_password(self, id_usuario, nuevo_hash):
        if self.usuario.id_usuario == id_usuario:
            self.usuario.contrasena = nuevo_hash
        return self.usuario

    def update_auth_fields(self, id_usuario, intentos_fallidos, bloqueado_hasta):
        if self.usuario.id_usuario == id_usuario:
            self.usuario.intentos_fallidos = intentos_fallidos
            self.usuario.bloqueado_hasta = bloqueado_hasta
        return self.usuario


def crear_usuario(estado="ACTIVO"):
    return SimpleNamespace(
        id_usuario=9,
        correo="usuario@test.com",
        contrasena="hash-viejo",
        estado=estado,
        motivo_bloqueo="Fraude" if estado == "BLOQUEADO" else None,
        fecha_bloqueo="2026-01-02 10:30:00" if estado == "BLOQUEADO" else None,
        intentos_fallidos=5,
        bloqueado_hasta="2026-01-02 11:00:00",
    )


def crear_caso_uso(usuario=None):
    repository = Mock()
    auth_repository = Mock()
    registro_repository = Mock()

    if usuario is not None:
        repository.get_by_id.return_value = usuario

    caso_uso = RestablecerPasswordUsuario(
        repository,
        auth_repository,
        registro_repository,
    )

    return caso_uso, repository, auth_repository, registro_repository


def test_no_permite_restablecer_la_password_propia():
    caso_uso, repository, auth_repository, registro_repository = crear_caso_uso()

    with pytest.raises(NoPuedeRestablecerPasswordPropiaException):
        caso_uso.execute(5, id_admin=5)

    repository.get_by_id.assert_not_called()
    auth_repository.invalidate_user_tokens.assert_not_called()
    repository.update_password.assert_not_called()
    registro_repository.registrar.assert_not_called()


def test_usuario_inexistente_lanza_404():
    caso_uso, repository, auth_repository, registro_repository = crear_caso_uso()
    repository.get_by_id.return_value = None

    with pytest.raises(UsuarioNotFoundException):
        caso_uso.execute(99, id_admin=1)

    auth_repository.invalidate_user_tokens.assert_not_called()
    repository.update_password.assert_not_called()
    repository.update_auth_fields.assert_not_called()
    registro_repository.registrar.assert_not_called()


def test_restablece_password_tokens_y_auditoria():
    usuario = crear_usuario()
    caso_uso, repository, auth_repository, registro_repository = crear_caso_uso(
        usuario
    )

    resultado = caso_uso.execute(9, id_admin=1)

    repository.get_by_id.assert_called_once_with(9)
    auth_repository.invalidate_user_tokens.assert_called_once_with(9)

    repository.update_password.assert_called_once()
    id_usuario, nuevo_hash = repository.update_password.call_args.args
    assert id_usuario == 9
    assert nuevo_hash != usuario.contrasena
    assert PasswordHasher.verify(usuario.contrasena, nuevo_hash) is False

    repository.update_auth_fields.assert_called_once_with(9, 0, None)

    auth_repository.create_recovery_token.assert_called_once()
    usuario_id_token, token_hash, fecha_expiracion = (
        auth_repository.create_recovery_token.call_args.args
    )
    assert usuario_id_token == 9
    assert token_hash == TokenGenerator.hash(resultado["token"])
    assert fecha_expiracion.tzinfo is not None

    ahora = datetime.now(timezone.utc)
    assert timedelta(minutes=MINUTOS_TOKEN_RECUPERACION - 1) < (
        fecha_expiracion - ahora
    ) <= timedelta(minutes=MINUTOS_TOKEN_RECUPERACION)

    registro_repository.registrar.assert_called_once_with(
        id_admin=1,
        accion=ACCION_RESTABLECER_PASSWORD,
        id_usuario_afectado=9,
        detalle=(
            "Contraseña invalidada y enlace de restablecimiento "
            "generado; intentos reiniciados"
        ),
    )

    assert set(resultado) == {"id_usuario", "correo", "token"}
    assert resultado["id_usuario"] == 9
    assert resultado["correo"] == "usuario@test.com"
    assert "contrasena" not in resultado


@patch(
    "app.modules.usuario.application.use_cases."
    "restablecer_password_usuario.PasswordHasher"
)
@patch(
    "app.modules.usuario.application.use_cases."
    "restablecer_password_usuario.secrets.token_urlsafe"
)
def test_genera_hash_aleatorio_sin_password_temporal(
    mock_token_urlsafe,
    mock_password_hasher,
):
    mock_token_urlsafe.return_value = "valor-aleatorio"
    mock_password_hasher.hash.return_value = "hash-aleatorio"

    usuario = crear_usuario()
    repository = Mock()
    repository.get_by_id.return_value = usuario

    caso_uso = RestablecerPasswordUsuario(
        repository,
        Mock(),
        Mock(),
    )

    caso_uso.execute(9, id_admin=1)

    mock_token_urlsafe.assert_any_call(32)
    mock_password_hasher.hash.assert_called_once_with("valor-aleatorio")
    repository.update_password.assert_called_once_with(
        9,
        "hash-aleatorio",
    )


@pytest.mark.parametrize("estado", ["BLOQUEADO", "INACTIVO"])
def test_restablece_sin_cambiar_el_estado_ni_el_bloqueo(estado):
    usuario = crear_usuario(estado)
    estado_original = usuario.estado
    motivo_original = usuario.motivo_bloqueo
    fecha_original = usuario.fecha_bloqueo
    repository = UsuarioRepositoryFake(usuario)
    caso_uso = RestablecerPasswordUsuario(repository, Mock(), Mock())

    caso_uso.execute(9, id_admin=1)

    assert usuario.estado == estado_original
    assert usuario.motivo_bloqueo == motivo_original
    assert usuario.fecha_bloqueo == fecha_original
    assert usuario.intentos_fallidos == 0
    assert usuario.bloqueado_hasta is None


def test_el_token_creado_sirve_para_confirmar_la_recuperacion():
    usuario = crear_usuario()
    usuario.contrasena = PasswordHasher.hash("ClaveVieja1!")
    repository = UsuarioRepositoryFake(usuario)
    auth_repository = AuthRepositoryFake()
    caso_uso = RestablecerPasswordUsuario(
        repository,
        auth_repository,
        Mock(),
    )

    resultado = caso_uso.execute(9, id_admin=1)

    assert PasswordHasher.verify("ClaveVieja1!", usuario.contrasena) is False

    confirmar = ConfirmPasswordRecoveryUseCase(auth_repository, repository)
    confirmar.execute(resultado["token"], "ClaveNueva1!")

    assert PasswordHasher.verify("ClaveNueva1!", usuario.contrasena) is True
    token = auth_repository.tokens[TokenGenerator.hash(resultado["token"])]
    assert token.usado is True


def test_reintento_invalida_el_token_anterior_y_genera_otro():
    usuario = crear_usuario()
    repository = UsuarioRepositoryFake(usuario)
    auth_repository = AuthRepositoryFake()
    caso_uso = RestablecerPasswordUsuario(
        repository,
        auth_repository,
        Mock(),
    )

    primero = caso_uso.execute(9, id_admin=1)
    segundo = caso_uso.execute(9, id_admin=1)

    assert primero["token"] != segundo["token"]
    assert auth_repository.tokens[
        TokenGenerator.hash(primero["token"])
    ].usado is True
    assert auth_repository.tokens[
        TokenGenerator.hash(segundo["token"])
    ].usado is False
