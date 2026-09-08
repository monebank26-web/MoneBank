from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database.connection import get_db
from app.core.security.auth import get_current_user
from app.modules.control_parental.application.use_cases.gestionar_mesada import GestionarMesada
from app.modules.control_parental.infrastructure.repository.sql_mesada_parental_repository import SqlMesadaParentalRepository
from app.modules.control_parental.presentation.schema.mesada_parental_schema import MesadaResponse, MesadaUpdate

router = APIRouter(prefix="/control-parental/dashboard", tags=["Gestión de mesadas"])


def get_repository(db: Session = Depends(get_db)):
    return SqlMesadaParentalRepository(db)


def error_http(error):
    if isinstance(error, PermissionError):
        return HTTPException(status_code=403, detail=str(error))
    return HTTPException(status_code=400, detail=str(error))


@router.put("/hijos/{id_hijo}/mesada", response_model=MesadaResponse)
def actualizar_mesada(
    id_hijo: int,
    data: MesadaUpdate,
    current_user=Depends(get_current_user),
    repository=Depends(get_repository),
):
    try:
        return GestionarMesada(repository).actualizar(
            current_user.id_usuario,
            id_hijo,
            data.model_dump(exclude_unset=True),
        )
    except (PermissionError, ValueError) as error:
        raise error_http(error) from error


@router.delete("/hijos/{id_hijo}/mesada", response_model=MesadaResponse)
def cancelar_mesada(
    id_hijo: int,
    current_user=Depends(get_current_user),
    repository=Depends(get_repository),
):
    try:
        return GestionarMesada(repository).cancelar(
            current_user.id_usuario,
            id_hijo,
        )
    except (PermissionError, ValueError) as error:
        raise error_http(error) from error
