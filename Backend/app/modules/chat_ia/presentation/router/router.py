from fastapi import APIRouter, Depends

from app.core.security.auth import get_current_user

from app.modules.chat_ia.presentation.controller.chat_controller import (
    ChatIaController,
    get_chat_ia_controller,
)
from app.modules.chat_ia.presentation.schema.chat_schema import (
    ChatResponse,
    EnviarMensajeRequest,
)


router = APIRouter(
    prefix="/chat-ia",
    tags=["Chat IA"],
)


@router.post("/mensaje", response_model=ChatResponse, status_code=200)
def enviar_mensaje(
    request: EnviarMensajeRequest,
    current_user: object = Depends(get_current_user),
    controller: ChatIaController = Depends(get_chat_ia_controller),
):
    return controller.enviar_mensaje(request, current_user)
