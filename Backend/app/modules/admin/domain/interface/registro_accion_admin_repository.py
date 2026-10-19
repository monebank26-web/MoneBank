from abc import ABC, abstractmethod


class RegistroAccionAdminRepository(ABC):

    @abstractmethod
    def registrar(
        self,
        id_admin,
        accion,
        id_usuario_afectado=None,
        detalle=None,
    ):
        pass

    @abstractmethod
    def listar(self, limite=50):
        pass
