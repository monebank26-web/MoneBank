from datetime import datetime, timedelta, timezone

import pytest

from app.modules.auth.domain.entity.reset_token import ResetToken


def test_token_es_valido():
    # Arrange
    token = ResetToken(
        id=1,
        usuario_id=1,
        token_hash="abc123",
        fecha_creacion=datetime.now(timezone.utc),
        fecha_expiracion=datetime.now(timezone.utc) + timedelta(minutes=15),
        usado=False
    )

    # Act & Assert
    assert token.es_valido() is True
    assert token.esta_expirado() is False
    assert token.fue_utilizado() is False


def test_token_expirado():
    # Arrange
    token = ResetToken(
        id=1,
        usuario_id=1,
        token_hash="abc123",
        fecha_creacion=datetime.now(timezone.utc) - timedelta(minutes=20),
        fecha_expiracion=datetime.now(timezone.utc) - timedelta(minutes=5),
        usado=False
    )

    # Act & Assert
    assert token.esta_expirado() is True
    assert token.es_valido() is False


def test_token_ya_usado():
    # Arrange
    token = ResetToken(
        id=1,
        usuario_id=1,
        token_hash="abc123",
        fecha_creacion=datetime.now(timezone.utc),
        fecha_expiracion=datetime.now(timezone.utc) + timedelta(minutes=15),
        usado=True
    )

    # Act & Assert
    assert token.fue_utilizado() is True
    assert token.es_valido() is False


def test_token_no_es_valido():
    # Arrange
    token = ResetToken(
        id=1,
        usuario_id=1,
        token_hash="abc123",
        fecha_creacion=datetime.now(timezone.utc) - timedelta(minutes=20),
        fecha_expiracion=datetime.now(timezone.utc) - timedelta(minutes=5),
        usado=True
    )

    # Act & Assert
    assert token.es_valido() is False
    assert token.esta_expirado() is True
    assert token.fue_utilizado() is True
