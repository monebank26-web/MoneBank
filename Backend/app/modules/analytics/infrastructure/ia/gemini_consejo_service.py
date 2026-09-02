import json
import logging
import time

from google import genai
from google.genai import types

from app.modules.analytics.domain.interface.consejo_ia_port import ConsejoIAPort
from app.shared.exceptions.business_exceptions import ConsejoIANoDisponible


MAX_REINTENTOS = 3
ESPERA_INICIAL_SEG = 1.0


PROMPT_BASE = (
    "Eres el asesor financiero de MoneBank. Analiza el gasto registrado junto "
    "con el comportamiento financiero reciente del usuario y genera un análisis "
    "claro, útil y conciso. Es OBLIGATORIO que la respuesta tenga EXACTAMENTE 2 "
    "párrafos y una extensión estricta de entre 120 y 160 palabras. "
    "Usa únicamente los datos proporcionados y no inventes cifras.\n\n"
    "Prioriza los 2 o 3 hallazgos financieros más relevantes, por ejemplo: "
    "variación frente al mes anterior, comparación con el promedio reciente, "
    "peso de la categoría sobre los gastos, frecuencia de compras o posible "
    "tendencia futura. Incluye siempre las cifras y datos numéricos explícitos. "
    "Asegúrate de que la explicación sea lógicamente coherente sin cruzar "
    "métricas que resulten contradictorias.\n\n"
    "Explica qué significan esos datos para el bolsillo del usuario y finaliza "
    "con una recomendación concreta y realista. Usa un lenguaje super sencillo "
    "y cotidiano (evita 'desembolso', 'liquidez', 'dinámica', 'rubro' o 'traslados'; "
    "prefiere 'gasto', 'categoría' o 'viajes'). Evita saludos, introducciones largas, "
    "repeticiones y frases genéricas. Usa un tono cercano, directo y educativo en español."
)

PROMPT_PREVIO = (
    "Eres el asesor financiero de MoneBank. El usuario está por registrar un "
    "gasto. Genera un análisis financiero complementario, claro y conciso. "
    "La respuesta debe tener OBLIGATORIO que la respuesta tenga EXACTAMENTE 2 párrafos "
    "y una extensión estricta de entre 120 y 160 palabras. Usa únicamente los datos "
    "proporcionados y no inventes cifras.\n\n"
    "El modal ya muestra el saldo restante y el impacto sobre el saldo y el "
    "límite, por lo que NO repitas esos porcentajes ni esa información. "
    "Analiza los 2 o 3 aspectos más relevantes del comportamiento financiero "
    "del usuario, como la variación frente al mes anterior, el promedio reciente, "
    "la importancia de la categoría, la frecuencia de gasto o una tendencia "
    "posible. Incluye siempre las cifras y datos numéricos explícitos. "
    "Asegúrate de que la explicación sea lógicamente coherente sin cruzar "
    "métricas que resulten contradictorias.\n\n"
    "Explica qué implica este gasto dentro de sus hábitos actuales y termina "
    "con una recomendación práctica y realista. Usa un lenguaje super sencillo "
    "y cotidiano (evita 'desembolso', 'liquidez', 'dinámica', 'rubro' o 'traslados'; "
    "prefiere 'gasto', 'categoría' o 'viajes'). Evita saludos, introducciones, "
    "repeticiones y frases genéricas. Usa un tono cercano, directo y educativo en español."
)


def _es_error_transitorio(error):
    codigo = getattr(getattr(error, "error", None), "code", None)
    if codigo is None:
        codigo = getattr(error, "code", None)
    return codigo in (429, 503)


class GeminiConsejoService(ConsejoIAPort):

    def __init__(self, api_key, modelo):
        self.api_key = api_key
        self.modelo = modelo
        self._client = None

    def _get_client(self):
        if self._client is None:
            self._client = genai.Client(api_key=self.api_key)
        return self._client

    def generar_consejo(self, contexto, es_previo=False):
        if not self.api_key:
            raise ConsejoIANoDisponible()

        prompt = PROMPT_PREVIO if es_previo else PROMPT_BASE
        cliente = self._get_client()
        ultimo_error = None

        for intento in range(MAX_REINTENTOS):
            try:
                respuesta = cliente.models.generate_content(
                    model=self.modelo,
                    contents=self._armar_prompt(contexto, prompt),
                    config=types.GenerateContentConfig(max_output_tokens=500),
                )
                return self._extraer_texto(respuesta)
            except ConsejoIANoDisponible:
                raise
            except Exception as e:
                ultimo_error = e
                if not _es_error_transitorio(e):
                    break
                if intento < MAX_REINTENTOS - 1:
                    time.sleep(ESPERA_INICIAL_SEG * (2 ** intento))

        if ultimo_error is not None:
            logging.error("Error consultando Gemini: %s", ultimo_error)
        raise ConsejoIANoDisponible()

    def _armar_prompt(self, contexto, prompt_base=PROMPT_BASE):
        return prompt_base + "\n" + json.dumps(contexto, ensure_ascii=False)

    def _extraer_texto(self, respuesta):
        texto = getattr(respuesta, "text", None)

        if not texto or not texto.strip():
            raise ConsejoIANoDisponible()

        return texto.strip()
