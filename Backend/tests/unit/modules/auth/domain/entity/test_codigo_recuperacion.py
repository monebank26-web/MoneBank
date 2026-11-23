from datetime import datetime, timedelta, timezone

from app.core.constants import MAX_INTENTOS_CODIGO_RECUPERACION
from app.modules.auth.domain.entity.reset_token import ResetToken


def test_codigo_es_valido():
    codigo = ResetToken(
        id=1,
        usuario_id=1,
        token_hash="abc123",
        fecha_creacion=datetime.now(timezone.utc),
        fecha_expiracion=datetime.now(timezone.utc) + timedelta(minutes=15),
        usado=False
    )

    assert codigo.es_valido() is True
    assert codigo.esta_expirado() is False
    assert codigo.fue_utilizado() is False


def test_codigo_expirado():
    codigo = ResetToken(
        id=1,
        usuario_id=1,
        token_hash="abc123",
        fecha_creacion=datetime.now(timezone.utc) - timedelta(minutes=20),
        fecha_expiracion=datetime.now(timezone.utc) - timedelta(minutes=5),
        usado=False
    )

    assert codigo.esta_expirado() is True
    assert codigo.es_valido() is False


def test_codigo_ya_usado():
    codigo = ResetToken(
        id=1,
        usuario_id=1,
        token_hash="abc123",
        fecha_creacion=datetime.now(timezone.utc),
        fecha_expiracion=datetime.now(timezone.utc) + timedelta(minutes=15),
        usado=True
    )

    assert codigo.fue_utilizado() is True
    assert codigo.es_valido() is False


def test_codigo_no_es_valido():
    codigo = ResetToken(
        id=1,
        usuario_id=1,
        token_hash="abc123",
        fecha_creacion=datetime.now(timezone.utc) - timedelta(minutes=20),
        fecha_expiracion=datetime.now(timezone.utc) - timedelta(minutes=5),
        usado=True
    )

    assert codigo.es_valido() is False
    assert codigo.esta_expirado() is True
    assert codigo.fue_utilizado() is True


def test_codigo_registra_intentos_fallidos():
    codigo = ResetToken(
        id=1,
        usuario_id=1,
        token_hash="abc123",
        fecha_expiracion=datetime.now(timezone.utc) + timedelta(minutes=15),
    )

    codigo.registrar_intento_fallido()

    assert codigo.intentos_fallidos == 1
    assert codigo.usado is False
    assert codigo.es_valido() is True


def test_codigo_se_marca_usado_al_llegar_al_maximo_de_intentos():
    codigo = ResetToken(
        id=1,
        usuario_id=1,
        token_hash="abc123",
        fecha_expiracion=datetime.now(timezone.utc) + timedelta(minutes=15),
        intentos_fallidos=MAX_INTENTOS_CODIGO_RECUPERACION - 1,
    )

    codigo.registrar_intento_fallido()

    assert codigo.intentos_fallidos == MAX_INTENTOS_CODIGO_RECUPERACION
    assert codigo.esta_agotado() is True
    assert codigo.usado is True
    assert codigo.es_valido() is False
