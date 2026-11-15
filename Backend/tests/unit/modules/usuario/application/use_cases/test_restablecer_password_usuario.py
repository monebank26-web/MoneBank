from datetime import datetime, timedelta, timezone
from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from app.core.constants import (
    MINUTOS_TOKEN_RECUPERACION,
    SEGUNDOS_ENFRIAMIENTO_CODIGO_RECUPERACION,
)
from app.core.security.PasswordHasher import PasswordHasher
from app.modules.auth.application.use_cases.codigo_recuperacion import (
    crear_codigo_recuperacion,
    hash_codigo_recuperacion,
)
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
    SolicitudCodigoRecienteException,
)


class AuthRepositoryFake:

    def __init__(self):
        self.tokens = {}
        self._siguiente_id = 1

    def invalidate_user_tokens(self, usuario_id):
        for token in self.tokens.values():
            if token.usuario_id == usuario_id:
                token.usado = True

    def find_latest_recovery_token(self, usuario_id):
        del_usuario = [
            token
            for token in self.tokens.values()
            if token.usuario_id == usuario_id
        ]

        if not del_usuario:
            return None

        return max(del_usuario, key=lambda token: token.id)

    def exists_recovery_token_hash(self, token_hash):
        return token_hash in self.tokens

    def create_recovery_token(
        self,
        usuario_id,
        token_hash,
        fecha_expiracion,
        intentos_fallidos=0,
    ):
        token = ResetToken(
            id=self._siguiente_id,
            usuario_id=usuario_id,
            token_hash=token_hash,
            fecha_creacion=datetime.now(timezone.utc),
            fecha_expiracion=fecha_expiracion,
            usado=False,
            intentos_fallidos=intentos_fallidos,
        )
        self.tokens[token_hash] = token
        self._siguiente_id += 1
        return token

    def find_valid_token(self, usuario_id, token_hash):
        token = self.tokens.get(token_hash)

        if (
            token
            and token.usuario_id == usuario_id
            and token.es_valido()
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

    def get_by_email_recuperacion(self, correo):
        if self.usuario.correo.lower() == correo.strip().lower():
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


def crear_generador(auth_repository):
    return lambda id_usuario: crear_codigo_recuperacion(
        auth_repository,
        id_usuario,
    )


def crear_caso_uso(usuario=None, auth_repository=None, generar_codigo=None):
    repository = Mock()
    registro_repository = Mock()

    if usuario is not None:
        repository.get_by_id.return_value = usuario

    if auth_repository is None:
        auth_repository = AuthRepositoryFake()

    if generar_codigo is None:
        generar_codigo = crear_generador(auth_repository)

    caso_uso = RestablecerPasswordUsuario(
        repository,
        registro_repository,
        generar_codigo,
    )

    return caso_uso, repository, auth_repository, registro_repository


def test_no_permite_restablecer_la_password_propia():
    generar_codigo = Mock()
    caso_uso, repository, _, registro_repository = crear_caso_uso(
        generar_codigo=generar_codigo
    )

    with pytest.raises(NoPuedeRestablecerPasswordPropiaException):
        caso_uso.execute(5, id_admin=5)

    repository.get_by_id.assert_not_called()
    generar_codigo.assert_not_called()
    repository.update_password.assert_not_called()
    registro_repository.registrar.assert_not_called()


def test_usuario_inexistente_lanza_404():
    generar_codigo = Mock()
    caso_uso, repository, _, registro_repository = crear_caso_uso(
        generar_codigo=generar_codigo
    )
    repository.get_by_id.return_value = None

    with pytest.raises(UsuarioNotFoundException):
        caso_uso.execute(99, id_admin=1)

    generar_codigo.assert_not_called()
    repository.update_password.assert_not_called()
    repository.update_auth_fields.assert_not_called()
    registro_repository.registrar.assert_not_called()


def test_genera_codigo_sin_cambiar_password_ni_intentos():
    usuario = crear_usuario()
    caso_uso, repository, auth_repository, registro_repository = crear_caso_uso(
        usuario
    )

    resultado = caso_uso.execute(9, id_admin=1)

    repository.get_by_id.assert_called_once_with(9)
    repository.update_password.assert_not_called()
    repository.update_auth_fields.assert_not_called()
    assert usuario.contrasena == "hash-viejo"
    assert usuario.intentos_fallidos == 5
    assert usuario.bloqueado_hasta == "2026-01-02 11:00:00"

    assert len(resultado["codigo"]) == 6
    assert resultado["codigo"].isdigit() is True

    token_hash = hash_codigo_recuperacion(9, resultado["codigo"])
    token = auth_repository.tokens[token_hash]
    assert token.usado is False
    assert token.intentos_fallidos == 0
    assert token.fecha_expiracion.tzinfo is not None

    ahora = datetime.now(timezone.utc)
    assert timedelta(minutes=MINUTOS_TOKEN_RECUPERACION - 1) < (
        token.fecha_expiracion - ahora
    ) <= timedelta(minutes=MINUTOS_TOKEN_RECUPERACION)

    registro_repository.registrar.assert_called_once_with(
        id_admin=1,
        accion=ACCION_RESTABLECER_PASSWORD,
        id_usuario_afectado=9,
        detalle=(
            "Código de restablecimiento generado; contraseña vigente"
        ),
    )

    assert set(resultado) == {"id_usuario", "correo", "codigo"}
    assert resultado["id_usuario"] == 9
    assert resultado["correo"] == "usuario@test.com"
    assert "contrasena" not in resultado


@pytest.mark.parametrize("estado", ["BLOQUEADO", "INACTIVO"])
def test_no_cambia_estado_bloqueo_ni_intentos(estado):
    usuario = crear_usuario(estado)
    estado_original = usuario.estado
    motivo_original = usuario.motivo_bloqueo
    fecha_original = usuario.fecha_bloqueo
    repository = UsuarioRepositoryFake(usuario)
    caso_uso = RestablecerPasswordUsuario(
        repository,
        Mock(),
        Mock(return_value="123456"),
    )

    caso_uso.execute(9, id_admin=1)

    assert usuario.estado == estado_original
    assert usuario.motivo_bloqueo == motivo_original
    assert usuario.fecha_bloqueo == fecha_original
    assert usuario.intentos_fallidos == 5
    assert usuario.bloqueado_hasta == "2026-01-02 11:00:00"


def test_el_codigo_creado_sirve_para_confirmar_la_recuperacion():
    usuario = crear_usuario()
    usuario.contrasena = PasswordHasher.hash("ClaveVieja1!")
    repository = UsuarioRepositoryFake(usuario)
    auth_repository = AuthRepositoryFake()
    caso_uso = RestablecerPasswordUsuario(
        repository,
        Mock(),
        crear_generador(auth_repository),
    )

    resultado = caso_uso.execute(9, id_admin=1)

    assert PasswordHasher.verify("ClaveVieja1!", usuario.contrasena) is True

    confirmar = ConfirmPasswordRecoveryUseCase(auth_repository, repository)
    confirmar.execute(
        usuario.correo,
        resultado["codigo"],
        "ClaveNueva1!",
    )

    assert PasswordHasher.verify("ClaveVieja1!", usuario.contrasena) is False
    assert PasswordHasher.verify("ClaveNueva1!", usuario.contrasena) is True

    token_hash = hash_codigo_recuperacion(9, resultado["codigo"])
    assert auth_repository.tokens[token_hash].usado is True


def test_reintento_invalida_el_codigo_anterior_y_genera_otro():
    usuario = crear_usuario()
    repository = UsuarioRepositoryFake(usuario)
    auth_repository = AuthRepositoryFake()
    caso_uso = RestablecerPasswordUsuario(
        repository,
        Mock(),
        crear_generador(auth_repository),
    )

    primero = caso_uso.execute(9, id_admin=1)
    token_primero = auth_repository.tokens[
        hash_codigo_recuperacion(9, primero["codigo"])
    ]
    token_primero.fecha_creacion = (
        datetime.now(timezone.utc)
        - timedelta(seconds=SEGUNDOS_ENFRIAMIENTO_CODIGO_RECUPERACION + 1)
    )

    segundo = caso_uso.execute(9, id_admin=1)

    assert primero["codigo"] != segundo["codigo"]
    assert auth_repository.tokens[
        hash_codigo_recuperacion(9, primero["codigo"])
    ].usado is True
    assert auth_repository.tokens[
        hash_codigo_recuperacion(9, segundo["codigo"])
    ].usado is False


def test_enfriamiento_lanza_solicitud_codigo_reciente():
    usuario = crear_usuario()
    repository = UsuarioRepositoryFake(usuario)
    auth_repository = AuthRepositoryFake()
    caso_uso = RestablecerPasswordUsuario(
        repository,
        Mock(),
        crear_generador(auth_repository),
    )

    caso_uso.execute(9, id_admin=1)

    with pytest.raises(SolicitudCodigoRecienteException):
        caso_uso.execute(9, id_admin=1)
