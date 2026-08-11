from abc import ABC, abstractmethod

class TransaccionRepository(ABC):

    @abstractmethod
    def find_by_usuario(
        self,
        db,
        usuario_id
    ):
        pass