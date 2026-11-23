from typing import Optional
from datetime import date

from fastapi import Depends

from app.core.config.settings import settings
from app.core.database.unit_of_work import UnitOfWork
from app.core.dependencies.repositories import get_unit_of_work
from app.modules.analytics.application.use_cases.generar_reporte import GenerarReporte
from app.modules.analytics.application.use_cases.obtener_consejo_ia import (
    ObtenerConsejoIA,
)
from app.modules.analytics.application.use_cases.obtener_consejo_previo import (
    ObtenerConsejoPrevio,
)
from app.modules.analytics.application.use_cases.obtener_graficas import (
    ObtenerGraficas,
)
from app.modules.analytics.application.use_cases.obtener_resumen_semanal import (
    ObtenerResumenSemanal,
)
from app.modules.analytics.domain.interface.analytics_repository import (
    AnalyticsRepository,
)
from app.modules.analytics.domain.interface.consejo_ia_port import ConsejoIAPort
from app.modules.analytics.infrastructure.ia.gemini_consejo_service import (
    GeminiConsejoService,
)
from app.modules.analytics.presentation.schema.consejo_previo_schema import (
    ConsejoPrevioRequest,
    ConsejoPrevioResponse,
)
from app.modules.analytics.presentation.schema.consejo_schema import ConsejoResponse
from app.shared.exceptions.chat_ia_errors import ConsejoIANoDisponible


CONSEJO_GENERICO = (
    "Lleva un registro constante de tus gastos y compáralos con tus límites "
    "cada semana para mantener el control de tu dinero."
)


class AnalyticsController:

    def __init__(
        self,
        repository: AnalyticsRepository,
        unit_of_work: UnitOfWork,
        consejo_ia: ConsejoIAPort,
    ):
        self.repository = repository
        self.unit_of_work = unit_of_work
        self.consejo_ia = consejo_ia

    def obtener_consejo_ia(self, id_transaccion: int, current_user):
        caso_uso = ObtenerConsejoIA(
            self.repository,
            self.unit_of_work.cuentas,
            self.consejo_ia,
        )

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

    def obtener_consejo_previo(
        self,
        request: ConsejoPrevioRequest,
        current_user,
    ):
        caso_uso = ObtenerConsejoPrevio(
            self.repository,
            self.unit_of_work.cuentas,
            self.consejo_ia,
        )

        try:
            consejo = caso_uso.execute(
                current_user.id_usuario,
                request.monto,
                request.id_categoria,
            )
            generado_con_ia = True
        except ConsejoIANoDisponible:
            consejo = CONSEJO_GENERICO
            generado_con_ia = False

        return ConsejoPrevioResponse(
            consejo=consejo,
            generado_con_ia=generado_con_ia,
        )

    def obtener_graficas(self, current_user, periodo: Optional[str] = None):
        return ObtenerGraficas(self.repository).execute(
            current_user.id_usuario,
            periodo,
        )

    def obtener_resumen_semanal(
        self,
        current_user,
        fecha_inicio: Optional[date] = None,
        fecha_fin: Optional[date] = None,
    ):
        return ObtenerResumenSemanal(self.repository).execute(
            current_user.id_usuario,
            fecha_inicio,
            fecha_fin,
        )

    def generar_reporte(
        self,
        current_user,
        periodo: Optional[str] = "mensual",
        fecha_inicio: Optional[date] = None,
        fecha_fin: Optional[date] = None,
    ):
        return GenerarReporte(self.repository).execute(
            current_user.id_usuario,
            periodo,
            fecha_inicio,
            fecha_fin,
        )


def get_consejo_ia_service() -> ConsejoIAPort:
    return GeminiConsejoService(settings.GOOGLE_AI_API_KEY, settings.GEMINI_MODEL)


def get_analytics_controller(
    unit_of_work: UnitOfWork = Depends(get_unit_of_work),
    consejo_ia: ConsejoIAPort = Depends(get_consejo_ia_service),
) -> AnalyticsController:
    return AnalyticsController(unit_of_work.analiticas, unit_of_work, consejo_ia)
