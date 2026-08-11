from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt

from app.core.config.settings import settings


class JwtManager:

    @staticmethod
    def create_token(
        data: dict,
        expires_minutes: int = None
    ) -> str:

        expire_min = (
            expires_minutes or
            settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

        payload = dict(data)
        payload["exp"] = (
            datetime.now(timezone.utc) +
            timedelta(minutes=expire_min)
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
