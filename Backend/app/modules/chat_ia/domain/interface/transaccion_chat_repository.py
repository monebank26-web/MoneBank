from abc import ABC, abstractmethod
from datetime import date


class TransaccionChatRepository(ABC):

    @abstractmethod
    def sumar_ingresos(self, id_usuario, desde: date):
        pass

    @abstractmethod
    def sumar_gastos(self, id_usuario, desde: date):
        pass

    @abstractmethod
    def top_categorias(self, id_usuario, desde: date, limite: int):
        pass
