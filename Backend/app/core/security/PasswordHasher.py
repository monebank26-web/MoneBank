import bcrypt


class PasswordHasher:

    @staticmethod
    def hash(password: str) -> str:
        password_bytes = password.encode("utf-8")[:72]
        hashed = bcrypt.hashpw(
            password_bytes,
            bcrypt.gensalt()
        )
        return hashed.decode("utf-8")

    @staticmethod
    def verify(
        plainPassword: str,
        hashedPassword: str
    ) -> bool:
        password_bytes = plainPassword.encode("utf-8")[:72]
        return bcrypt.checkpw(
            password_bytes,
            hashedPassword.encode("utf-8")
        )
