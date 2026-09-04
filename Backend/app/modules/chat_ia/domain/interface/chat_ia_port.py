from abc import ABC, abstractmethod


class ChatIAPort(ABC):

    @abstractmethod
    def generar_respuesta(self, contexto_financiero: dict, contenidos_gemini: list) -> str:
        pass
