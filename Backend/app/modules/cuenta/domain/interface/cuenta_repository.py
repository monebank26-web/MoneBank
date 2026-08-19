from abc import ABC, abstractmethod


class CuentaRepository(ABC):

    @abstractmethod
    def create(self, cuenta_data):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def get_by_id(self, id_cuenta):
        pass

    @abstractmethod
    def delete(self, id_cuenta):
        pass
