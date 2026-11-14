from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.config.settings import settings
from app.core.database.unit_of_work import UnitOfWork
from app.core.database.connection import get_db
from app.core.dependencies.repositories import get_unit_of_work
from app.modules.chat_ia.application.use_cases.enviar_mensaje_chat import (
    EnviarMensajeChat,
)
from app.modules.chat_ia.domain.interface.chat_ia_port import ChatIAPort
from app.modules.chat_ia.domain.interface.transaccion_chat_repository import (
    TransaccionChatRepository,
)
from app.modules.chat_ia.infrastructure.ia.gemini_chat_service import GeminiChatService
from app.modules.chat_ia.infrastructure.repository.transaccion_chat_repository import (
    SqlTransaccionChatRepository,
)
from app.modules.chat_ia.presentation.schema.chat_schema import ChatResponse
from app.modules.cuenta.domain.interface.cuenta_repository import CuentaRepository
from app.shared.exceptions.chat_ia_errors import ConsejoIANoDisponible


RESPUESTA_GENERICA = (
    "Para planear mejor tu dinero, registra tus gastos e ingresos y compara "
    "tu avance con tus metas cada semana."
)


def get_transaccion_chat_repository(
    db: Session = Depends(get_db),
) -> TransaccionChatRepository:
    return SqlTransaccionChatRepository(db)


def get_chat_ia_service() -> ChatIAPort:
    return GeminiChatService(settings.GOOGLE_AI_API_KEY, settings.GEMINI_MODEL)


class ChatIaController:

    def __init__(
        self,
        cuenta_repository: CuentaRepository,
        unit_of_work: UnitOfWork,
        transaccion_chat_repository: TransaccionChatRepository,
        chat_ia: ChatIAPort,
    ):
        self.cuenta_repository = cuenta_repository
        self.unit_of_work = unit_of_work
        self.transaccion_chat_repository = transaccion_chat_repository
        self.chat_ia = chat_ia

    def enviar_mensaje(self, request, current_user):
        caso_uso = EnviarMensajeChat(
            self.cuenta_repository,
            self.unit_of_work.ahorros,
            self.transaccion_chat_repository,
            self.chat_ia,
        )

        try:
            respuesta = caso_uso.execute(
                current_user.id_usuario,
                request.mensaje,
                [t.model_dump() for t in request.historial],
            )
            return ChatResponse(respuesta=respuesta, generado_con_ia=True)
        except ConsejoIANoDisponible:
            return ChatResponse(respuesta=RESPUESTA_GENERICA, generado_con_ia=False)


def get_chat_ia_controller(
    unit_of_work: UnitOfWork = Depends(get_unit_of_work),
    transaccion_chat_repository: TransaccionChatRepository = Depends(
        get_transaccion_chat_repository
    ),
    chat_ia: ChatIAPort = Depends(get_chat_ia_service),
) -> ChatIaController:
    return ChatIaController(
        unit_of_work.cuentas,
        unit_of_work,
        transaccion_chat_repository,
        chat_ia,
    )
