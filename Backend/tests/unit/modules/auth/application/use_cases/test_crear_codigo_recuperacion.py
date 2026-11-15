from datetime import datetime, timedelta, timezone
from unittest.mock import patch

from app.core.constants import (
    MINUTOS_TOKEN_RECUPERACION,
    SEGUNDOS_ENFRIAMIENTO_CODIGO_RECUPERACION,
)
from app.modules.auth.application.use_cases.codigo_recuperacion import (
    crear_codigo_recuperacion,
    generar_codigo_recuperacion,
    hash_codigo_recuperacion,
)
from app.modules.auth.domain.entity.reset_token import ResetToken


class AuthRepositoryFake:

    def __init__(self, ultimo=None, hashes_existentes=None):
        self.ultimo = ultimo
        self.hashes_existentes = set(hashes_existentes or [])
        self.invalidaciones = []
        self.creaciones = []

    def find_latest_recovery_token(self, usuario_id):
        return self.ultimo

    def invalidate_user_tokens(self, usuario_id):
        self.invalidaciones.append(usuario_id)

    def exists_recovery_token_hash(self, token_hash):
        return token_hash in self.hashes_existentes

    def create_recovery_token(self, usuario_id, token_hash, fecha_expiracion):
        self.creaciones.append(
            (usuario_id, token_hash, fecha_expiracion)
        )
        return SimpleToken(
            usuario_id=usuario_id,
            token_hash=token_hash,
            fecha_expiracion=fecha_expiracion,
        )


class SimpleToken:

    def __init__(self, usuario_id, token_hash, fecha_expiracion):
        self.usuario_id = usuario_id
        self.token_hash = token_hash
        self.fecha_expiracion = fecha_expiracion
        self.usado = False


def test_generar_codigo_recuperacion_tiene_seis_digitos_y_ceros_a_la_izquierda():
    with patch(
        "app.modules.auth.application.use_cases.codigo_recuperacion."
        "secrets.randbelow",
        return_value=42,
    ):
        codigo = generar_codigo_recuperacion()

    assert codigo == "000042"
    assert len(codigo) == 6


def test_hash_codigo_recuperacion_incluye_el_id_del_usuario():
    hash_uno = hash_codigo_recuperacion(1, "123456")
    hash_dos = hash_codigo_recuperacion(2, "123456")

    assert hash_uno != hash_dos


def test_crear_codigo_recuperacion_invalida_el_anterior_y_crea_el_nuevo():
    repository = AuthRepositoryFake()

    with patch(
        "app.modules.auth.application.use_cases.codigo_recuperacion."
        "secrets.randbelow",
        return_value=42,
    ):
        codigo = crear_codigo_recuperacion(repository, 9)

    assert codigo == "000042"
    assert repository.invalidaciones == [9]
    assert len(repository.creaciones) == 1

    usuario_id, token_hash, fecha_expiracion = repository.creaciones[0]
    assert usuario_id == 9
    assert token_hash == hash_codigo_recuperacion(9, "000042")
    assert fecha_expiracion.tzinfo is not None

    ahora = datetime.now(timezone.utc)
    assert timedelta(minutes=MINUTOS_TOKEN_RECUPERACION - 1) < (
        fecha_expiracion - ahora
    ) <= timedelta(minutes=MINUTOS_TOKEN_RECUPERACION)


def test_crear_codigo_recuperacion_devuelve_none_en_enfriamiento():
    repository = AuthRepositoryFake(
        ultimo=ResetToken(
            id=1,
            usuario_id=9,
            token_hash="hash",
            fecha_creacion=datetime.now(timezone.utc),
            fecha_expiracion=(
                datetime.now(timezone.utc) + timedelta(minutes=15)
            ),
        )
    )

    resultado = crear_codigo_recuperacion(repository, 9)

    assert resultado is None
    assert repository.invalidaciones == []
    assert repository.creaciones == []


def test_crear_codigo_recuperacion_permite_generar_despues_del_enfriamiento():
    fecha_vieja = (
        datetime.now(timezone.utc)
        - timedelta(seconds=SEGUNDOS_ENFRIAMIENTO_CODIGO_RECUPERACION + 1)
    )
    repository = AuthRepositoryFake(
        ultimo=ResetToken(
            id=1,
            usuario_id=9,
            token_hash="hash",
            fecha_creacion=fecha_vieja,
            fecha_expiracion=(
                datetime.now(timezone.utc) + timedelta(minutes=15)
            ),
        )
    )

    with patch(
        "app.modules.auth.application.use_cases.codigo_recuperacion."
        "secrets.randbelow",
        return_value=7,
    ):
        resultado = crear_codigo_recuperacion(repository, 9)

    assert resultado == "000007"
    assert repository.invalidaciones == [9]
    assert len(repository.creaciones) == 1


def test_crear_codigo_recuperacion_reintenta_si_el_hash_ya_existe():
    hash_ocupado = hash_codigo_recuperacion(9, "000001")
    repository = AuthRepositoryFake(hashes_existentes={hash_ocupado})

    with patch(
        "app.modules.auth.application.use_cases.codigo_recuperacion."
        "secrets.randbelow",
        side_effect=[1, 2],
    ):
        resultado = crear_codigo_recuperacion(repository, 9)

    assert resultado == "000002"
    assert len(repository.creaciones) == 1
    assert repository.creaciones[0][1] == hash_codigo_recuperacion(9, "000002")
