from abc import ABC, abstractmethod


class AhorroRepository(ABC):

    @abstractmethod
    def create(self, ahorro_data):
        pass

    @abstractmethod
    def get_all(self):
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
