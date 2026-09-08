from typing import Literal

from pydantic import BaseModel, Field


class TurnoChat(BaseModel):
    rol: Literal["user", "model"]
    texto: str


class EnviarMensajeRequest(BaseModel):
    mensaje: str = Field(..., min_length=1, max_length=2000)
    historial: list[TurnoChat] = Field(default_factory=list, max_length=50)


class ChatResponse(BaseModel):
    respuesta: str
    generado_con_ia: bool
