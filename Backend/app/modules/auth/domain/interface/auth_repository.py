from abc import ABC, abstractmethod


class AuthRepository(ABC):

    @abstractmethod
    def login(self, correo):
        """Debe devolver el usuario que coincide con ese correo, o None."""
        pass

    @abstractmethod
    def register_failed_attempt(self, usuario_id):
        """Debe incrementar el contador de intentos fallidos del usuario,
        y bloquear la cuenta temporalmente si se alcanza el máximo permitido."""
        pass

    @abstractmethod
    def is_locked(self, usuario_id):
        """Debe devolver True si la cuenta del usuario sigue bloqueada
        en este momento, False en caso contrario."""
        pass

    @abstractmethod
    def reset_failed_attempts(self, usuario_id):
        """Debe poner a cero los intentos fallidos del usuario
        y limpiar el bloqueo temporal tras un login exitoso."""
        pass

    @abstractmethod
    def create_recovery_token(self, usuario_id, token_hash, fecha_expiracion):
        """Debe crear y persistir un token de recuperación de contraseña
        asociado al usuario indicado."""
        pass

    @abstractmethod
    def find_valid_token(self, token_hash):
        """Debe devolver el token de recuperación que coincida con el hash,
        que no esté expirado y que no haya sido utilizado, o None."""
        pass

    @abstractmethod
    def invalidate_token(self, token_id):
        """Debe marcar un token de recuperación como utilizado."""
        pass

    @abstractmethod
    def invalidate_user_tokens(self, usuario_id):
        """Debe invalidar todos los tokens de recuperación activos
        de un usuario (marcarlos como utilizados)."""
        pass
