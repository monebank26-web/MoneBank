from abc import ABC, abstractmethod



class ProgramacionAhorroRepository(ABC):

    @abstractmethod
    def create(self, programacion_data):
        pass

    @abstractmethod
    def update_estado(self, programacion_id, nuevo_estado):
        pass
    