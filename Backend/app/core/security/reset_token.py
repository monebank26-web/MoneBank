import hashlib
import secrets


class TokenGenerator:

    @staticmethod
    def generate() -> str:
        return secrets.token_urlsafe(32)

    @staticmethod
    def hash(token: str) -> str:
        return hashlib.sha256(token.encode()).hexdigest()
