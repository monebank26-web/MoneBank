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
