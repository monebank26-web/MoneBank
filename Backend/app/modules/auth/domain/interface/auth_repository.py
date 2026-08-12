from abc import ABC, abstractmethod


class AuthRepository(ABC):

    @abstractmethod
    def login(self, db, correo):
        """Debe devolver el usuario que coincide con ese correo, o None."""
        pass

    @abstractmethod
    def register_failed_attempt(self, db, usuario_id):
        """Debe incrementar el contador de intentos fallidos del usuario,
        y bloquear la cuenta temporalmente si se alcanza el máximo permitido."""
        pass

    @abstractmethod
    def is_locked(self, db, usuario_id):
        """Debe devolver True si la cuenta del usuario sigue bloqueada
        en este momento, False en caso contrario."""
        pass