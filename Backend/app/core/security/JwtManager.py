from datetime import datetime, timedelta, timezone

from jose import jwt

from app.core.config.settings import settings


class JwtManager:

    @staticmethod
    def create_token(
        data: dict,
        expires_minutes: int = None
    ) -> str:

        ahora = datetime.now(timezone.utc)
        iat = int(ahora.timestamp())
        payload = dict(data)
        payload.setdefault("iat", iat)
        payload.setdefault("orig_iat", payload["iat"])
        payload["exp"] = ahora + timedelta(
            minutes=expires_minutes or
            settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

        return jwt.encode(
            payload,
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM
        )

    @staticmethod
    def decode_token(token: str) -> dict:
        return jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

    @staticmethod
    def _a_datetime(valor) -> datetime:
        if isinstance(valor, datetime):
            if valor.tzinfo is None:
                return valor.replace(tzinfo=timezone.utc)
            return valor
        return datetime.fromtimestamp(float(valor), tz=timezone.utc)

    @staticmethod
    def _inicio(payload: dict) -> datetime:
        valor = payload.get("orig_iat") or payload.get("iat")
        if valor is None:
            return JwtManager._a_datetime(payload["exp"]) - timedelta(
                minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
            )
        return JwtManager._a_datetime(valor)

    @staticmethod
    def needs_renewal(payload: dict, ahora=None) -> bool:
        ahora = ahora or datetime.now(timezone.utc)
        exp = JwtManager._a_datetime(payload["exp"])
        tope = JwtManager._inicio(payload) + timedelta(
            hours=settings.TOKEN_ABSOLUTE_MAX_HOURS
        )
        return (
            ahora < exp <= ahora + timedelta(
                minutes=settings.TOKEN_RENEW_BEFORE_MINUTES
            )
            and tope - ahora > timedelta(
                minutes=settings.TOKEN_RENEW_BEFORE_MINUTES
            )
        )

    @staticmethod
    def renew_token(payload: dict) -> str:
        ahora = datetime.now(timezone.utc)
        inicio = JwtManager._inicio(payload)
        tope = inicio + timedelta(
            hours=settings.TOKEN_ABSOLUTE_MAX_HOURS
        )

        nuevo_payload = {
            clave: valor
            for clave, valor in payload.items()
            if clave not in ("exp", "iat", "nbf")
        }
        nuevo_payload["iat"] = int(ahora.timestamp())
        nuevo_payload["orig_iat"] = int(inicio.timestamp())
        nuevo_payload["exp"] = min(
            ahora + timedelta(
                minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
            ),
            tope,
        )

        return jwt.encode(
            nuevo_payload,
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM
        )
