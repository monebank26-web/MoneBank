from app.core.security.JwtManager import JwtManager
from app.core.security.PasswordHasher import PasswordHasher
from app.core.config.settings import settings
from app.shared.exceptions.business_exceptions import (InvalidCredentialsException, AccountLockedException )

class LoginUsuarioUseCase:

    def __init__(self, repository):
        self.repository = repository

    def execute(self, db, correo, contrasena):

        usuario = self.repository.login(db,correo)

        if not usuario:
            raise InvalidCredentialsException()

        if self.repository.is_locked(db, usuario.id_usuario):
            raise AccountLockedException()

        if not PasswordHasher.verify(contrasena, usuario.contrasena):
            self.repository.register_failed_attempt(db, usuario.id_usuario)
            raise InvalidCredentialsException()

        token = JwtManager.create_token({
            "sub": str(usuario.id_usuario),
            "correo": usuario.correo,
            "id_rol": usuario.id_rol,
        })

        return {
            "access_token": token,
            "token_type": "bearer",
            "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            "usuario_id": usuario.id_usuario,
        }