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
    "Eres el asesor financiero de MoneBank. Analiza este gasto junto con las "
    "estadísticas del mes del usuario y entrega un análisis extenso en 3 "
    "párrafos (unas 13-15 líneas). Usa el contexto para calcular y citar "
    "cifras y porcentajes que ayuden al usuario a dimensionar el impacto en "
    "los próximos 3 meses, sin inventar datos. Estructura el consejo así:\n"
    "1) Situación: cómo se compara este gasto/categoría con el promedio de 3 "
    "meses y con el mes anterior (por ejemplo, el incremento porcentual vs el "
    "mes pasado, y qué porcentaje de su gasto total representa).\n"
    "2) Tendencia: la frecuencia de este tipo de gasto (número de transacciones "
    "del mes y del anterior) y la proyección a 3 meses si mantiene este ritmo.\n"
    "3) Acción: un consejo práctico, concreto y accionable para mantener el "
    "control. Usa un tono cercano, directo y coloquial en español."
)

PROMPT_PREVIO = (
    "Eres el asesor financiero de MoneBank. El usuario va a registrar un gasto. "
    "El modal YA le mostró cuánto dinero le queda y cómo afecta SIEMPRE los "
    "porcentajes de saldo y de límite. Por eso NO repitas el porcentaje de "
    "saldo que consume el gasto ni el porcentaje usado/proyectado del límite. "
    "Entrega un análisis COMPLEMENTARIO extenso en 3 párrafos (unas 13-15 "
    "líneas) con cifras y porcentajes que el modal NO muestra, usando el "
    "contexto sin inventar datos. Estructúralo así:\n"
    "1) Tendencias de la categoría: compara el gasto de este mes con el del "
    "pasado (por ejemplo, el incremento porcentual mensual) y con su promedio "
    "de 3 meses.\n"
    "2) Impacto a 3 meses: qué porcentaje de su gasto total representa esta "
    "categoría y la proyección del gasto en los próximos 3 meses si mantiene "
    "este ritmo, considerando la frecuencia de compras (transacciones del mes "
    "y del anterior).\n"
    "3) Recomendación: un consejo práctico, concreto y accionable. Sé directo, "
    "coloquial y motivador, en español."
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
                    config=types.GenerateContentConfig(max_output_tokens=700),
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
