from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.config.settings import settings
from app.core.database.connection import get_db
from app.core.security.auth import get_current_user
from app.modules.analytics.application.use_cases.obtener_consejo_ia import (
    ObtenerConsejoIA
)
from app.modules.analytics.domain.interface.analytics_repository import (
    AnalyticsRepository
)
from app.modules.analytics.domain.interface.consejo_ia_port import ConsejoIAPort
from app.modules.analytics.infrastructure.ia.gemini_consejo_service import (
    GeminiConsejoService
)
from app.modules.analytics.infrastructure.repository.sql_analytics_repository import (
    SqlAnalyticsRepository
)
from app.modules.analytics.presentation.schema.consejo_schema import ConsejoResponse
from app.shared.exceptions.business_exceptions import ConsejoIANoDisponible


router = APIRouter(
    prefix="/analitica",
    tags=["Analitica"]
)

CONSEJO_GENERICO = (
    "Lleva un registro constante de tus gastos y compáralos con tus límites "
    "cada semana para mantener el control de tu dinero."
)


def get_analytics_repository(db: Session = Depends(get_db)) -> AnalyticsRepository:
    return SqlAnalyticsRepository(db)


def get_consejo_ia_service() -> ConsejoIAPort:
    return GeminiConsejoService(settings.GOOGLE_AI_API_KEY, settings.GEMINI_MODEL)


@router.get(
    "/transacciones/{id_transaccion}/consejo",
    response_model=ConsejoResponse,
    status_code=200
)
def obtener_consejo_ia(
    id_transaccion: int,
    current_user: object = Depends(get_current_user),
    repository: AnalyticsRepository = Depends(get_analytics_repository),
    consejo_ia: ConsejoIAPort = Depends(get_consejo_ia_service),
):
    caso_uso = ObtenerConsejoIA(repository, consejo_ia)

    try:
        consejo = caso_uso.execute(current_user.id_usuario, id_transaccion)
        generado_con_ia = True
    except ConsejoIANoDisponible:
        consejo = CONSEJO_GENERICO
        generado_con_ia = False

    return ConsejoResponse(
        id_transaccion=id_transaccion,
        consejo=consejo,
        generado_con_ia=generado_con_ia,
    )
