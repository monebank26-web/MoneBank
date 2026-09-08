from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional
from datetime import date

from app.core.config.settings import settings
from app.core.database.connection import get_db
from app.core.security.auth import get_current_user
from app.modules.analytics.application.use_cases.obtener_consejo_ia import (
    ObtenerConsejoIA
)
from app.modules.analytics.application.use_cases.obtener_consejo_previo import (
    ObtenerConsejoPrevio
)
from app.modules.analytics.application.use_cases.obtener_graficas import (
    ObtenerGraficas
)
from app.modules.analytics.application.use_cases.obtener_resumen_semanal import (
    ObtenerResumenSemanal
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
from app.modules.analytics.presentation.schema.consejo_previo_schema import (
    ConsejoPrevioRequest,
    ConsejoPrevioResponse,
)
from app.modules.cuenta.domain.interface.cuenta_repository import CuentaRepository
from app.modules.cuenta.infrastructure.repository.sql_cuenta_repository import (
    SqlCuentaRepository
)
from app.modules.analytics.presentation.schema.grafica_schema import GraficaResponse
from app.modules.analytics.presentation.schema.resumen_semanal_schema import (
    ResumenSemanalResponse
)
from app.modules.analytics.application.use_cases.generar_reporte import GenerarReporte
from app.modules.analytics.presentation.schema.reporte_schema import ReporteResponse 
from app.shared.exceptions.business_exceptions import ConsejoIANoDisponible
from fastapi.responses import StreamingResponse
from app.modules.analytics.infrastructure.pdf.reporte_pdf_generator import (
    generar_pdf_reporte
)


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


def get_cuenta_repository(db: Session = Depends(get_db)) -> CuentaRepository:
    return SqlCuentaRepository(db)


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
    cuenta_repository: CuentaRepository = Depends(get_cuenta_repository),
    consejo_ia: ConsejoIAPort = Depends(get_consejo_ia_service),
):
    caso_uso = ObtenerConsejoIA(repository, cuenta_repository, consejo_ia)

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


@router.post(
    "/consejo-previo",
    response_model=ConsejoPrevioResponse,
    status_code=200
)
def obtener_consejo_previo(
    request: ConsejoPrevioRequest,
    current_user: object = Depends(get_current_user),
    repository: AnalyticsRepository = Depends(get_analytics_repository),
    cuenta_repository: CuentaRepository = Depends(get_cuenta_repository),
    consejo_ia: ConsejoIAPort = Depends(get_consejo_ia_service),
):
    caso_uso = ObtenerConsejoPrevio(repository, cuenta_repository, consejo_ia)

    try:
        consejo = caso_uso.execute(
            current_user.id_usuario, request.monto, request.id_categoria
        )
        generado_con_ia = True
    except ConsejoIANoDisponible:
        consejo = CONSEJO_GENERICO
        generado_con_ia = False

    return ConsejoPrevioResponse(
        consejo=consejo,
        generado_con_ia=generado_con_ia,
    )


@router.get(
    "/graficas",
    response_model=GraficaResponse,
    status_code=200,
    responses={401: {"description": "No autorizado"}, 500: {"description": "Error interno"}},
)
def obtener_graficas_endpoint(
    periodo: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: object = Depends(get_current_user)
):
    repo = SqlAnalyticsRepository(db)
    caso_uso = ObtenerGraficas(repo)
    return caso_uso.execute(current_user.id_usuario, periodo)


@router.get(
    "/resumen-semanal",
    response_model=ResumenSemanalResponse,
    status_code=200,
    responses={401: {"description": "No autorizado"}, 500: {"description": "Error interno"}},
)
def obtener_resumen_semanal_endpoint(
    fecha_inicio: Optional[date] = None,
    fecha_fin: Optional[date] = None,
    db: Session = Depends(get_db),
    current_user: object = Depends(get_current_user)
):
    repo = SqlAnalyticsRepository(db)
    caso_uso = ObtenerResumenSemanal(repo)
    return caso_uso.execute(current_user.id_usuario, fecha_inicio, fecha_fin)

@router.get(
    "/reportes",
    response_model=ReporteResponse,
    status_code=200,
    responses={401: {"description": "No autorizado"}, 500: {"description": "Error interno"}},
)
def obtener_reporte_endpoint(
    periodo: Optional[str] = "mensual",
    fecha_inicio: Optional[date] = None,
    fecha_fin: Optional[date] = None,
    db: Session = Depends(get_db),
    current_user: object = Depends(get_current_user)
):
    repo = SqlAnalyticsRepository(db)
    caso_uso = GenerarReporte(repo)
    return caso_uso.execute(current_user.id_usuario, periodo, fecha_inicio, fecha_fin)

@router.get("/reportes/pdf")
def descargar_reporte_pdf(
    periodo: Optional[str] = "mensual",
    fecha_inicio: Optional[date] = None,
    fecha_fin: Optional[date] = None,
    db: Session = Depends(get_db),
    current_user: object = Depends(get_current_user)
):
    repo = SqlAnalyticsRepository(db)
    caso_uso = GenerarReporte(repo)
    reporte = caso_uso.execute(current_user.id_usuario, periodo, fecha_inicio, fecha_fin)

    pdf_buffer = generar_pdf_reporte(reporte)
    nombre_archivo = f"reporte_{reporte['periodo_inicio']}_{reporte['periodo_fin']}.pdf"

    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={nombre_archivo}"}
    )