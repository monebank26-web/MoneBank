from abc import ABC, abstractmethod


class ConsejoIAPort(ABC):

    @abstractmethod
    def generar_consejo(self, contexto):
        pass
