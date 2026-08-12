from abc import ABC, abstractmethod

class TransaccionRepository(ABC):

    @abstractmethod
    def find_by_usuario(
        self,
        usuario_id
    ):
        pass