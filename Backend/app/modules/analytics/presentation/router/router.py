from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from app.core.security.auth import get_current_user

from app.modules.analytics.infrastructure.pdf.reporte_pdf_generator import (
    generar_pdf_reporte,
)
from app.modules.analytics.presentation.controller.analytics_controller import (
    AnalyticsController,
    get_analytics_controller,
)
from app.modules.analytics.presentation.schema.consejo_previo_schema import (
    ConsejoPrevioRequest,
    ConsejoPrevioResponse,
)
from app.modules.analytics.presentation.schema.consejo_schema import ConsejoResponse
from app.modules.analytics.presentation.schema.grafica_schema import GraficaResponse
from app.modules.analytics.presentation.schema.reporte_schema import ReporteResponse
from app.modules.analytics.presentation.schema.resumen_semanal_schema import (
    ResumenSemanalResponse,
)


router = APIRouter(
    prefix="/analitica",
    tags=["Analitica"]
)


@router.get(
    "/transacciones/{id_transaccion}/consejo",
    response_model=ConsejoResponse,
    status_code=200
)
def obtener_consejo_ia(
    id_transaccion: int,
    current_user: object = Depends(get_current_user),
    controller: AnalyticsController = Depends(get_analytics_controller),
):
    return controller.obtener_consejo_ia(id_transaccion, current_user)


@router.post(
    "/consejo-previo",
    response_model=ConsejoPrevioResponse,
    status_code=200
)
def obtener_consejo_previo(
    request: ConsejoPrevioRequest,
    current_user: object = Depends(get_current_user),
    controller: AnalyticsController = Depends(get_analytics_controller),
):
    return controller.obtener_consejo_previo(request, current_user)


@router.get(
    "/graficas",
    response_model=GraficaResponse,
    status_code=200,
    responses={401: {"description": "No autorizado"}, 500: {"description": "Error interno"}},
)
def obtener_graficas_endpoint(
    periodo: Optional[str] = None,
    current_user: object = Depends(get_current_user),
    controller: AnalyticsController = Depends(get_analytics_controller),
):
    return controller.obtener_graficas(current_user, periodo)


@router.get(
    "/resumen-semanal",
    response_model=ResumenSemanalResponse,
    status_code=200,
    responses={401: {"description": "No autorizado"}, 500: {"description": "Error interno"}},
)
def obtener_resumen_semanal_endpoint(
    fecha_inicio: Optional[date] = None,
    fecha_fin: Optional[date] = None,
    current_user: object = Depends(get_current_user),
    controller: AnalyticsController = Depends(get_analytics_controller),
):
    return controller.obtener_resumen_semanal(current_user, fecha_inicio, fecha_fin)


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
    current_user: object = Depends(get_current_user),
    controller: AnalyticsController = Depends(get_analytics_controller),
):
    return controller.generar_reporte(current_user, periodo, fecha_inicio, fecha_fin)


@router.get("/reportes/pdf")
def descargar_reporte_pdf(
    periodo: Optional[str] = "mensual",
    fecha_inicio: Optional[date] = None,
    fecha_fin: Optional[date] = None,
    current_user: object = Depends(get_current_user),
    controller: AnalyticsController = Depends(get_analytics_controller),
):
    reporte = controller.generar_reporte(current_user, periodo, fecha_inicio, fecha_fin)

    pdf_buffer = generar_pdf_reporte(reporte)
    nombre_archivo = f"reporte_{reporte['periodo_inicio']}_{reporte['periodo_fin']}.pdf"

    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={nombre_archivo}"}
    )
