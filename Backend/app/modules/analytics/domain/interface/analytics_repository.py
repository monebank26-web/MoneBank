from abc import ABC, abstractmethod


class AnalyticsRepository(ABC):

    @abstractmethod
    def find_transaccion(self, id_usuario, id_transaccion):
        pass

    @abstractmethod
    def calcular_stats_mes(self, id_usuario):
        pass

    @abstractmethod
    def get_saldo_cuenta(self, id_cuenta):
        pass

    @abstractmethod
    def get_cuenta_usuario(self, id_usuario):
        pass

    @abstractmethod
    def get_categoria_nombre(self, id_categoria):
        pass

    @abstractmethod
    def get_resumen_categoria(self, id_usuario, id_categoria):
        pass

    @abstractmethod
    def get_limite_categoria(self, id_usuario, id_categoria):
        pass
