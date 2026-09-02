from abc import ABC, abstractmethod


class AhorroRepository(ABC):

    @abstractmethod
    def create(self, ahorro_data):
        pass

    @abstractmethod
    def get_by_id(self, id_ahorro):
        pass

    @abstractmethod
    def update(self, id_ahorro, ahorro_data):
        pass

    @abstractmethod
    def delete(self, id_ahorro):
        pass

    @abstractmethod
    def get_tipo_ahorro(self, nombre):
        pass

    @abstractmethod
    def get_categoria(self, id_categoria):
        pass

    @abstractmethod
    def get_by_cuenta_y_tipo(self, id_cuenta, nombre_tipo_ahorro):
        pass

    @abstractmethod
    def get_metas_activas(self, id_cuenta):
        pass

    @abstractmethod
    def get_progreso(self, id_ahorro):
        pass

    @abstractmethod
    def get_gasto_periodo(self, id_categoria, id_cuenta, fecha_desde, fecha_hasta):
        pass

    @abstractmethod
    def get_by_cuenta(self, id_cuenta):
        pass
