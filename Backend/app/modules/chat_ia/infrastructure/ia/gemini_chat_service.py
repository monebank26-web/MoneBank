import json
import logging

from google import genai
from google.genai import types

from app.modules.chat_ia.domain.interface.chat_ia_port import ChatIAPort
from app.shared.exceptions.business_exceptions import ConsejoIANoDisponible


SYSTEM_INSTRUCTION_CHAT = (
    "Eres el asesor financiero de MoneBank. SOLO respondes preguntas sobre "
    "finanzas personales: presupuestos, ahorro, gastos, metas financieras, "
    "deudas y planeación financiera. Si te preguntan algo fuera de ese ámbito "
    "(código, tareas, salud, etc.), responde amablemente que solo puedes "
    "ayudar con temas financieros y redirige la conversación.\n"
    "Contexto financiero actual del usuario (json):\n{contexto}"
)


class GeminiChatService(ChatIAPort):

    def __init__(self, api_key, modelo):
        self.api_key = api_key
        self.modelo = modelo
        self._client = None

    def _get_client(self):
        if self._client is None:
            self._client = genai.Client(api_key=self.api_key)
        return self._client

    def generar_respuesta(self, contexto_financiero, contenidos_gemini):
        if not self.api_key:
            raise ConsejoIANoDisponible()

        system = SYSTEM_INSTRUCTION_CHAT.format(
            contexto=json.dumps(contexto_financiero, ensure_ascii=False)
        )
        cliente = self._get_client()
        try:
            respuesta = cliente.models.generate_content(
                model=self.modelo,
                contents=contenidos_gemini,
                config=types.GenerateContentConfig(
                    system_instruction=system,
                    max_output_tokens=700,
                ),
            )
            return self._extraer_texto(respuesta)
        except ConsejoIANoDisponible:
            raise
        except Exception as e:
            logging.error("Error consultando Gemini (chat): %s", e)
            raise ConsejoIANoDisponible()

    def _extraer_texto(self, respuesta):
        texto = getattr(respuesta, "text", None)
        if not texto or not texto.strip():
            raise ConsejoIANoDisponible()
        return texto.strip()
