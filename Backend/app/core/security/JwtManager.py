from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError

SECRET_KEY = "CAMBIAR_ESTO_POR_UNA_VARIABLE_DE_ENTORNO"  # ver nota abajo
ALGORITHM = "HS256"
EXPIRE_MINUTES = 60


class JwtManager:

    @staticmethod
    def create_token(data: dict, expires_minutes: int = EXPIRE_MINUTES) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    @staticmethod
    def decode_token(token: str) -> dict | None:
        try:
            return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except JWTError:
            return None