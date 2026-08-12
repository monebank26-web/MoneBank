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
    def get_by_email(self, correo):
        """Debe devolver el usuario que coincide con ese correo, o None."""
        pass

    @abstractmethod
    def reset_failed_attempts(self, usuario_id):
        """Debe poner a cero los intentos fallidos del usuario
        y limpiar el bloqueo temporal tras un login exitoso."""
        pass
