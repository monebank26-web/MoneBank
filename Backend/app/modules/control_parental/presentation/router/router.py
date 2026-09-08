from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database.connection import get_db
from app.core.security.auth import get_current_user
from app.core.dependencies.email_service import EmailService

from app.modules.control_parental.infrastructure.repository.sql_control_parental_repository import (
    SqlControlParentalRepository,
)

from app.modules.control_parental.application.use_cases.solicitar_vinculacion import (
    SolicitarVinculacionUseCase,
)

from app.modules.control_parental.application.use_cases.confirmar_vinculacion import (
    ConfirmarVinculacionUseCase,
)

from app.modules.control_parental.application.use_cases.solicitar_desvinculacion import (
    SolicitarDesvinculacionUseCase,
)

from app.modules.control_parental.application.use_cases.confirmar_desvinculacion import (
    ConfirmarDesvinculacionUseCase,
)

from app.modules.control_parental.application.use_cases.obtener_vinculaciones import (
    ObtenerVinculacionesUseCase,
)

from app.modules.control_parental.application.use_cases.dashboard_parental import (
    ListarHijosParentales,
    ObtenerResumenHijo,
    ObtenerTransaccionesHijo,
    ObtenerPermisosHijo,
    ActualizarPermisosHijo,
)

from app.modules.control_parental.presentation.schema.control_parental_schema import (
    HijoParentalResponse,
    ResumenHijoResponse,
    TransaccionParentalResponse,
    PermisoResponse,
    PermisosUpdate,
)

# Estos esquemas deben existir en tu archivo actual.
# Se conservan porque son utilizados por vinculación y desvinculación.
from app.modules.control_parental.presentation.schema.control_parental_schema import (
    SolicitarVinculacionRequest,
    ConfirmarCodigoRequest,
    SolicitarDesvinculacionRequest,
    RelacionResponse,
    SolicitudResponse,
)


router = APIRouter(
    prefix="/control-parental",
    tags=["Control parental"],
)


# ============================================================
# DEPENDENCIAS
# ============================================================

def get_parental_repository(
    db: Session = Depends(get_db),
):

    return SqlControlParentalRepository(db)


def get_email_service():
    return EmailService()


def manejar_error(error):
    status_code = getattr(error, "status_code", 403)

    detail = getattr(
        error,
        "message",
        str(error),
    )

    raise HTTPException(
        status_code=status_code,
        detail=detail,
    )


# ============================================================
# VINCULACIÓN
# ============================================================

@router.post(
    "/vinculaciones",
    status_code=201,
)
def solicitar_vinculacion(
    data: SolicitarVinculacionRequest,
    current_user=Depends(get_current_user),
    repository=Depends(get_parental_repository),
    email_service=Depends(get_email_service),
):
    """
    El padre solicita vincular una cuenta hija.
    """
    caso_uso = SolicitarVinculacionUseCase(
        repository=repository,
        email_service=email_service,
    )

    return caso_uso.execute(
        id_padre=current_user.id_usuario,
        nombre_hijo=data.nombre_hijo,
        correo_hijo=data.correo_hijo,
    )


@router.post(
    "/vinculaciones/confirmar",
    response_model=RelacionResponse,
)
def confirmar_vinculacion(
    data: ConfirmarCodigoRequest,
    current_user=Depends(get_current_user),
    repository=Depends(get_parental_repository),
):
    """
    El hijo confirma el código de vinculación.
    """
    caso_uso = ConfirmarVinculacionUseCase(repository)

    return caso_uso.execute(
        current_user.id_usuario,
        data.codigo,
    )


@router.get(
    "/vinculaciones",
    response_model=list[RelacionResponse],
)
def obtener_vinculaciones(
    current_user=Depends(get_current_user),
    repository=Depends(get_parental_repository),
):
    return ObtenerVinculacionesUseCase(
        repository
    ).execute(
        current_user.id_usuario
    )


# ============================================================
# DESVINCULACIÓN
# ============================================================

@router.post(
    "/desvinculaciones",
    response_model=SolicitudResponse,
    status_code=201,
)
def solicitar_desvinculacion(
    data: SolicitarDesvinculacionRequest,
    current_user=Depends(get_current_user),
    repository=Depends(get_parental_repository),
    email_service=Depends(get_email_service),
):
    """
    El hijo solicita desvincularse.

    El código se envía al correo del padre,
    pero el hijo lo introduce y confirma.
    """
    solicitud = SolicitarDesvinculacionUseCase(
        repository,
        email_service,
    ).execute(
        current_user.id_usuario,
        data.correo_padre,
    )

    return SolicitudResponse(
        mensaje="Código enviado al correo del padre",
        id_solicitud=solicitud.id_solicitud,
    )


@router.post(
    "/desvinculaciones/confirmar",
)
def confirmar_desvinculacion(
    data: ConfirmarCodigoRequest,
    current_user=Depends(get_current_user),
    repository=Depends(get_parental_repository),
):
    """
    El hijo confirma la desvinculación usando el código
    enviado al padre.
    """
    ConfirmarDesvinculacionUseCase(
        repository
    ).execute(
        current_user.id_usuario,
        data.codigo,
    )

    return {
        "mensaje": "Cuenta desvinculada correctamente"
    }


# ============================================================
# DASHBOARD DEL PADRE
# ============================================================

@router.get(
    "/dashboard/hijos",
    response_model=list[HijoParentalResponse],
)
def listar_hijos(
    current_user=Depends(get_current_user),
    repository=Depends(get_parental_repository)
,
):
    try:
        return ListarHijosParentales(
            repository
        ).execute(
            current_user.id_usuario
        )
    except Exception as error:
        manejar_error(error)


@router.get(
    "/dashboard/hijos/{id_hijo}/resumen",
    response_model=ResumenHijoResponse,
)
def obtener_resumen_hijo(
    id_hijo: int,
    current_user=Depends(get_current_user),
    repository=Depends(get_parental_repository)
,
):
    try:
        return ObtenerResumenHijo(
            repository
        ).execute(
            current_user.id_usuario,
            id_hijo,
        )
    except Exception as error:
        manejar_error(error)


@router.get(
    "/dashboard/hijos/{id_hijo}/transacciones",
    response_model=list[TransaccionParentalResponse],
)
def obtener_transacciones_hijo(
    id_hijo: int,
    limite: int = Query(
        default=20,
        ge=1,
        le=100,
    ),
    current_user=Depends(get_current_user),
    repository=Depends(get_parental_repository)
,
):
    try:
        return ObtenerTransaccionesHijo(
            repository
        ).execute(
            current_user.id_usuario,
            id_hijo,
            limite,
        )
    except Exception as error:
        manejar_error(error)


@router.get(
    "/dashboard/hijos/{id_hijo}/permisos",
    response_model=list[PermisoResponse],
)
def obtener_permisos_hijo(
    id_hijo: int,
    current_user=Depends(get_current_user),
    repository=Depends(get_parental_repository),
):
    try:
        return ObtenerPermisosHijo(
            repository
        ).execute(
            current_user.id_usuario,
            id_hijo,
        )
    except Exception as error:
        manejar_error(error)


@router.put(
    "/dashboard/hijos/{id_hijo}/permisos",
    response_model=list[PermisoResponse],
)
def actualizar_permisos_hijo(
    id_hijo: int,
    data: PermisosUpdate,
    current_user=Depends(get_current_user),
    repository=Depends(get_parental_repository),
):
    try:
        return ActualizarPermisosHijo(
            repository
        ).execute(
            current_user.id_usuario,
            id_hijo,
            data.permisos,
        )
    except Exception as error:
        manejar_error(error)
