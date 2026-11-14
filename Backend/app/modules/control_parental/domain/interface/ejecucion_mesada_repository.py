from abc import ABC, abstractmethod


class EjecucionMesadaRepository(ABC):

    @abstractmethod
    def vinculo_activo(self, id_padre, id_hijo):
        pass

    @abstractmethod
    def permiso_activo(self, id_control):
        pass

    @abstractmethod
    def mesada_activa_bloqueada(self, id_control):
        pass

    @abstractmethod
    def cuentas_bloqueadas(self, id_cuenta_padre, id_cuenta_hijo):
        pass

    @abstractmethod
    def ejecucion_periodo(self, id_mesada, periodo):
        pass

    @abstractmethod
    def obtener_tipo_transaccion(self, nombre):
        pass

    @abstractmethod
    def obtener_categoria(self, nombre, tipo_categoria):
        pass

    @abstractmethod
    def ejecutar(
        self,
        mesada,
        cuenta_padre,
        cuenta_hijo,
        periodo,
        proxima,
        id_tipo_salida,
        id_tipo_entrada,
        id_categoria_salida,
        id_categoria_entrada,
    ):
        pass

    @abstractmethod
    def rollback(self):
        pass
