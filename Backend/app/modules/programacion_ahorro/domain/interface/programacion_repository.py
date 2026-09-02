from abc import ABC, abstractmethod



class ProgramacionAhorroRepository(ABC):

    @abstractmethod
    def create(self, programacion_data):
        pass
