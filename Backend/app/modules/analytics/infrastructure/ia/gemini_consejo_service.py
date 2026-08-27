import json

import httpx

from app.modules.analytics.domain.interface.consejo_ia_port import ConsejoIAPort
import logging
from app.shared.exceptions.business_exceptions import ConsejoIANoDisponible


GEMINI_URL_BASE = "https://generativelanguage.googleapis.com/v1beta/models"
TIMEOUT_SEGUNDOS = 30

PROMPT_BASE = (
    "Eres un asesor financiero de MoneBank. Con este gasto y las estadísticas "
    "del mes del usuario, da un consejo breve de máximo 3 frases, práctico, "
    "concreto y motivador. No inventes datos que no están en el contexto."
)

PROMPT_PREVIO = (
    "Eres el asesor financiero de MoneBank. El usuario va a registrar un gasto. "
    "El modal YA le mostró cuánto dinero le queda y cómo afecta sus límites. "
    "NO repitas esos números. Da un análisis COMPLEMENTARIO breve (2-3 frases) "
    "sobre: patrón de gasto vs sus hábitos, tendencia este mes vs anterior, "
    "y un consejo práctico y accionable. Sé directo y coloquial."
)


class GeminiConsejoService(ConsejoIAPort):

    def __init__(self, api_key, modelo):
        self.api_key = api_key
        self.modelo = modelo

    def generar_consejo(self, contexto, es_previo=False):
        if not self.api_key:
            raise ConsejoIANoDisponible()

        prompt = PROMPT_PREVIO if es_previo else PROMPT_BASE

        try:
            respuesta = httpx.post(
                f"{GEMINI_URL_BASE}/{self.modelo}:generateContent",
                headers={"x-goog-api-key": self.api_key},
                json={
                    "contents": [
                        {"parts": [{"text": self._armar_prompt(contexto, prompt)}]}
                    ],
                    "generationConfig": {
                        "maxOutputTokens": 200
                    }
                },
                timeout=TIMEOUT_SEGUNDOS,
            )
            return self._extraer_texto(respuesta)
        except ConsejoIANoDisponible:
            raise
        except Exception as e:
            logging.error("Error consultando Gemini: %s", e)
            raise ConsejoIANoDisponible()

    def _armar_prompt(self, contexto, prompt_base=PROMPT_BASE):
        return prompt_base + "\n" + json.dumps(contexto, ensure_ascii=False)

    def _extraer_texto(self, respuesta):
        data = respuesta.json()
        texto = (
            data.get("candidates", [{}])[0]
            .get("content", {})
            .get("parts", [{}])[0]
            .get("text")
        )

        if not texto or not texto.strip():
            raise ConsejoIANoDisponible()

        return texto.strip()
