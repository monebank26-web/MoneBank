from abc import ABC, abstractmethod



class ProgramacionAhorroRepository(ABC):

    @abstractmethod
    def create(self, programacion_data):
        pass

    @abstractmethod
    def obtener_por_ahorro(self, id_ahorro):
        pass

    @abstractmethod
    def update_estado(self, programacion_id, nuevo_estado):
        pass

    @abstractmethod
    def obtener_detalles_por_cuenta(self, id_cuenta):
        pass
    