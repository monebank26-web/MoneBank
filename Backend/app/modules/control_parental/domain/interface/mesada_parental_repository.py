from abc import ABC, abstractmethod


class MesadaParentalRepository(ABC):

    @abstractmethod
    def obtener_vinculo_activo(self, id_padre, id_hijo):
        pass

    @abstractmethod
    def permiso_activo(self, id_control, nombre_permiso):
        pass

    @abstractmethod
    def obtener_cuentas(self, id_padre, id_hijo):
        pass

    @abstractmethod
    def obtener_activa(self, id_control):
        pass

    @abstractmethod
    def crear(self, model):
        pass

    @abstractmethod
    def guardar(self):
        pass

    @staticmethod
    def model_to_dict(model):
        pass
