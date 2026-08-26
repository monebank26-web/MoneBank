import json

import httpx

from app.modules.analytics.domain.interface.consejo_ia_port import ConsejoIAPort
from app.shared.exceptions.business_exceptions import ConsejoIANoDisponible


GEMINI_URL_BASE = "https://generativelanguage.googleapis.com/v1beta/models"
TIMEOUT_SEGUNDOS = 10

PROMPT_BASE = (
    "Eres un asesor financiero de MoneBank. Con este gasto y las estadísticas "
    "del mes del usuario, da un consejo breve de máximo 3 frases, práctico, "
    "concreto y motivador. No inventes datos que no están en el contexto."
)


class GeminiConsejoService(ConsejoIAPort):

    def __init__(self, api_key, modelo):
        self.api_key = api_key
        self.modelo = modelo

    def generar_consejo(self, contexto):
        if not self.api_key:
            raise ConsejoIANoDisponible()

        try:
            respuesta = httpx.post(
                f"{GEMINI_URL_BASE}/{self.modelo}:generateContent",
                headers={"x-goog-api-key": self.api_key},
                json={
                    "contents": [
                        {"parts": [{"text": self._armar_prompt(contexto)}]}
                    ]
                },
                timeout=TIMEOUT_SEGUNDOS,
            )
            return self._extraer_texto(respuesta)
        except ConsejoIANoDisponible:
            raise
        except Exception:
            raise ConsejoIANoDisponible()

    def _armar_prompt(self, contexto):
        return PROMPT_BASE + "\n" + json.dumps(contexto, ensure_ascii=False)

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
