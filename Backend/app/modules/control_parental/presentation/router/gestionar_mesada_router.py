from fastapi import APIRouter, Depends, HTTPException

from app.core.database.unit_of_work import UnitOfWork
from app.core.dependencies.repositories import get_unit_of_work
from app.core.security.auth import get_current_user
from app.modules.control_parental.application.use_cases.gestionar_mesada import GestionarMesada
from app.modules.control_parental.presentation.schema.mesada_parental_schema import MesadaResponse, MesadaUpdate

router = APIRouter(prefix="/control-parental/dashboard", tags=["Gestión de mesadas"])


def error_http(error):
    if isinstance(error, PermissionError):
        return HTTPException(status_code=403, detail=str(error))
    return HTTPException(status_code=400, detail=str(error))


@router.put("/hijos/{id_hijo}/mesada", response_model=MesadaResponse)
def actualizar_mesada(
    id_hijo: int,
    data: MesadaUpdate,
    current_user=Depends(get_current_user),
    unit_of_work: UnitOfWork = Depends(get_unit_of_work),
):
    try:
        resultado = GestionarMesada(unit_of_work.mesadas).actualizar(
            current_user.id_usuario,
            id_hijo,
            data.model_dump(exclude_unset=True),
        )
        unit_of_work.commit()
        return resultado
    except (PermissionError, ValueError) as error:
        raise error_http(error) from error


@router.delete("/hijos/{id_hijo}/mesada", response_model=MesadaResponse)
def cancelar_mesada(
    id_hijo: int,
    current_user=Depends(get_current_user),
    unit_of_work: UnitOfWork = Depends(get_unit_of_work),
):
    try:
        resultado = GestionarMesada(unit_of_work.mesadas).cancelar(
            current_user.id_usuario,
            id_hijo,
        )
        unit_of_work.commit()
        return resultado
    except (PermissionError, ValueError) as error:
        raise error_http(error) from error
