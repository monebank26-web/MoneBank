from datetime import datetime, timedelta, timezone
import secrets
from app.core.security.reset_token import TokenGenerator

MINUTOS_EXPIRACION = 15

def generar_codigo_seis_digitos():
    return f"{secrets.randbelow(1_000_000):06d}"

def hash_codigo(codigo):
    return TokenGenerator.hash(codigo)

def expiracion_codigo():
    return datetime.now(timezone.utc) + timedelta(minutes=MINUTOS_EXPIRACION)
