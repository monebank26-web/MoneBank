import secrets
from datetime import datetime, timedelta, timezone

from app.core.constants import (
    MINUTOS_TOKEN_RECUPERACION,
    SEGUNDOS_ENFRIAMIENTO_CODIGO_RECUPERACION,
)
from app.core.security.reset_token import TokenGenerator


def generar_codigo_recuperacion() -> str:
    return f"{secrets.randbelow(1_000_000):06d}"


def hash_codigo_recuperacion(usuario_id, codigo: str) -> str:
    return TokenGenerator.hash(f"{usuario_id}:{codigo}")


def crear_codigo_recuperacion(auth_repository, usuario_id):
    """Genera y persiste un código de recuperación.

    Devuelve None cuando el último código del usuario se creó hace menos de
    SEGUNDOS_ENFRIAMIENTO_CODIGO_RECUPERACION segundos.
    """
    ultimo = auth_repository.find_latest_recovery_token(usuario_id)
    ahora = datetime.now(timezone.utc)

    if ultimo and ultimo.fecha_creacion:
        fecha_creacion = ultimo.fecha_creacion

        if fecha_creacion.tzinfo is None:
            fecha_creacion = fecha_creacion.replace(tzinfo=timezone.utc)

        if (ahora - fecha_creacion).total_seconds() < (
            SEGUNDOS_ENFRIAMIENTO_CODIGO_RECUPERACION
        ):
            return None

    auth_repository.invalidate_user_tokens(usuario_id)

    fecha_expiracion = (
        ahora + timedelta(minutes=MINUTOS_TOKEN_RECUPERACION)
    )

    while True:
        codigo = generar_codigo_recuperacion()
        token_hash = hash_codigo_recuperacion(usuario_id, codigo)

        if auth_repository.exists_recovery_token_hash(token_hash):
            continue

        auth_repository.create_recovery_token(
            usuario_id,
            token_hash,
            fecha_expiracion,
            intentos_fallidos=0,
        )
        return codigo
