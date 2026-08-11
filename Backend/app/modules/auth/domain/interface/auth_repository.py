from abc import ABC, abstractmethod


class AuthRepository(ABC):

    @abstractmethod
    def login(self, db, correo):
        """Debe devolver el usuario que coincide con ese correo, o None."""
        pass