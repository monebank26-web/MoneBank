from passlib.context import CryptContext

pwdContext = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


class PasswordHasher:

    @staticmethod
    def hash(password: str) -> str:
        return pwdContext.hash(password)

    @staticmethod
    def verify(
        plainPassword: str,
        hashedPassword: str
    ) -> bool:
        return pwdContext.verify(
            plainPassword,
            hashedPassword
        )