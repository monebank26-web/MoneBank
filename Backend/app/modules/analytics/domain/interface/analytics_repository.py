from abc import ABC, abstractmethod


class AnalyticsRepository(ABC):

    @abstractmethod
    def find_transaccion(self, id_usuario, id_transaccion):
        pass

    @abstractmethod
    def calcular_stats_mes(self, id_usuario):
        pass

    @abstractmethod
    def get_categoria_nombre(self, id_categoria):
        pass

    @abstractmethod
    def get_resumen_categoria(self, id_usuario, id_categoria):
        pass

    @abstractmethod
    def get_limite_categoria(self, id_cuenta, id_categoria):
        pass

    @abstractmethod
    def obtener_datos_grafica(self, id_usuario, periodo=None):
        pass

    @abstractmethod
    def obtener_movimientos_periodo(self, id_usuario, fecha_inicio, fecha_fin):
        pass

    @abstractmethod
    def obtener_movimientos_periodo(self, id_usuario, fecha_inicio, fecha_fin):
        pass

    @abstractmethod
    def obtener_reporte_periodo(self, id_usuario, fecha_inicio, fecha_fin):
         pass 