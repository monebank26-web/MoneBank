from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.config.settings import settings
from app.core.database.connection import get_db
from app.core.security.auth import get_current_user
from app.modules.ahorro.domain.interface.ahorro_repository import AhorroRepository
from app.modules.ahorro.infrastructure.repository.sql_ahorro_repository import (
    SqlAhorroRepository
)
from app.modules.chat_ia.application.use_cases.enviar_mensaje_chat import (
    EnviarMensajeChat
)
from app.modules.chat_ia.domain.interface.chat_ia_port import ChatIAPort
from app.modules.chat_ia.domain.interface.transaccion_chat_repository import (
    TransaccionChatRepository
)
from app.modules.chat_ia.infrastructure.ia.gemini_chat_service import (
    GeminiChatService
)
from app.modules.chat_ia.infrastructure.repository.transaccion_chat_repository import (
    SqlTransaccionChatRepository
)
from app.modules.chat_ia.presentation.schema.chat_schema import (
    ChatResponse,
    EnviarMensajeRequest,
)
from app.modules.cuenta.domain.interface.cuenta_repository import CuentaRepository
from app.modules.cuenta.infrastructure.repository.sql_cuenta_repository import (
    SqlCuentaRepository
)
from app.shared.exceptions.business_exceptions import ConsejoIANoDisponible


router = APIRouter(
    prefix="/chat-ia",
    tags=["Chat IA"],
)

RESPUESTA_GENERICA = (
    "Para planear mejor tu dinero, registra tus gastos e ingresos y compara "
    "tu avance con tus metas cada semana."
)


def get_cuenta_repository(db: Session = Depends(get_db)) -> CuentaRepository:
    return SqlCuentaRepository(db)


def get_ahorro_repository(db: Session = Depends(get_db)) -> AhorroRepository:
    return SqlAhorroRepository(db)


def get_transaccion_chat_repository(
    db: Session = Depends(get_db),
) -> TransaccionChatRepository:
    return SqlTransaccionChatRepository(db)


def get_chat_ia_service() -> ChatIAPort:
    return GeminiChatService(settings.GOOGLE_AI_API_KEY, settings.GEMINI_MODEL)


def _armar_respuesta(mensaje, historial, id_usuario, cuenta_repo, ahorro_repo, transacc_repo, chat_ia):
    caso_uso = EnviarMensajeChat(cuenta_repo, ahorro_repo, transacc_repo, chat_ia)
    try:
        respuesta = caso_uso.execute(
            id_usuario,
            mensaje,
            [t.model_dump() for t in historial],
        )
        return ChatResponse(respuesta=respuesta, generado_con_ia=True)
    except ConsejoIANoDisponible:
        return ChatResponse(respuesta=RESPUESTA_GENERICA, generado_con_ia=False)


@router.post("/mensaje", response_model=ChatResponse, status_code=200)
def enviar_mensaje(
    request: EnviarMensajeRequest,
    current_user: object = Depends(get_current_user),
    cuenta_repo: CuentaRepository = Depends(get_cuenta_repository),
    ahorro_repo: AhorroRepository = Depends(get_ahorro_repository),
    transacc_repo: TransaccionChatRepository = Depends(get_transaccion_chat_repository),
    chat_ia: ChatIAPort = Depends(get_chat_ia_service),
):
    return _armar_respuesta(
        request.mensaje,
        request.historial,
        current_user.id_usuario,
        cuenta_repo,
        ahorro_repo,
        transacc_repo,
        chat_ia,
    )
