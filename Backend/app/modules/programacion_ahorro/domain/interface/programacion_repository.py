from abc import ABC, abstractmethod



class ProgramacionAhorroRepository(ABC):

    @abstractmethod
    def create(self, programacion_data):
        pass

    @abstractmethod
    def get_by_id(self, programacion_id):
        pass

    @abstractmethod
    def get_para_procesar(self, programacion_id):
        pass

    @abstractmethod
    def obtener_vencidas(self, hoy):
        pass

    @abstractmethod
    def actualizar_fecha_cobro(
        self,
        programacion_id,
        nueva_fecha,
        nuevo_estado=None,
    ):
        pass

    @abstractmethod
    def obtener_por_ahorro(self, id_ahorro):
        pass

    @abstractmethod
    def update_estado(self, programacion_id, nuevo_estado):
        pass

    @abstractmethod
    def update_periodicidad(self, programacion_id, monto_periodico, frecuencia):
        pass

    @abstractmethod
    def obtener_detalles_por_cuenta(self, id_cuenta):
        pass
