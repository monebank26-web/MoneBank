from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database.connection import get_db
from app.core.security.auth import get_current_user
from app.modules.control_parental.application.use_cases.configurar_mesada import ConfigurarMesada
from app.modules.control_parental.application.use_cases.obtener_mesada import ObtenerMesada
from app.modules.control_parental.infrastructure.repository.sql_mesada_parental_repository import SqlMesadaParentalRepository
from app.modules.control_parental.presentation.schema.mesada_parental_schema import MesadaCreate, MesadaResponse

router = APIRouter(prefix="/control-parental/dashboard", tags=["Mesadas parentales"])


def get_repository(db: Session = Depends(get_db)):
    return SqlMesadaParentalRepository(db)


def manejar_error(error):
    raise HTTPException(
        status_code=getattr(error, "status_code", 403),
        detail=getattr(error, "message", str(error)),
    )


@router.post("/hijos/{id_hijo}/mesada", response_model=MesadaResponse, status_code=201)
def crear_mesada(
    id_hijo: int,
    data: MesadaCreate,
    current_user=Depends(get_current_user),
    repository=Depends(get_repository),
):
    try:
        return ConfigurarMesada(repository).execute(
            current_user.id_usuario,
            id_hijo,
            data.model_dump(),
        )
    except Exception as error:
        manejar_error(error)


@router.get("/hijos/{id_hijo}/mesada", response_model=MesadaResponse | None)
def obtener_mesada(
    id_hijo: int,
    current_user=Depends(get_current_user),
    repository=Depends(get_repository),
):
    try:
        return ObtenerMesada(repository).execute(
            current_user.id_usuario,
            id_hijo,
        )
    except Exception as error:
        manejar_error(error)
