from abc import ABC, abstractmethod


class TransaccionRepository(ABC):

    @abstractmethod
    def find_historial(self, usuario_id, filtros):
        pass

    @abstractmethod
    def find_categorias(self):
        pass

    @abstractmethod
    def create(self, transaccion_data):
        pass

    @abstractmethod
    def get_cuenta(self, id_cuenta):
        pass

    @abstractmethod
    def existe_categoria(self, id_categoria):
        pass

    @abstractmethod
    def get_tipo_transaccion(self, nombre):
        pass

    @abstractmethod
    def get_ahorro(self, id_ahorro):
        pass

    @abstractmethod
    def descontar_saldo(self, id_cuenta, monto):
        pass
