from abc import ABC, abstractmethod


class CuentaRepository(ABC):

    @abstractmethod
    def create(self, cuenta_data):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def get_cuenta_por_usuario(self, id_usuario):
        pass

    @abstractmethod
    def get_cuenta_por_id(self, id_cuenta):
        pass

    @abstractmethod
    def update(self, id_cuenta, cuenta_data):
        pass

    @abstractmethod
    def actualizar_saldo(self, id_cuenta, monto):
        pass

    @abstractmethod
    def delete(self, id_cuenta):
        pass