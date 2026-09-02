from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database.connection import get_db
from app.core.security.auth import get_current_user

from app.modules.programacion_ahorro.application.crear_programacion import CrearProgramacion
from app.modules.programacion_ahorro.domain.interface.programacion_repository import ProgramacionAhorroRepository
from app.modules.programacion_ahorro.infrastructure.repository.sql_programacion_repository import SqlProgramacionRepository
from app.modules.programacion_ahorro.presentation.schema.programacion_schema import (
    ProgramacionCreate,
    ProgramacionResponse,
)

from app.modules.cuenta.domain.interface.cuenta_repository import CuentaRepository
from app.modules.cuenta.infrastructure.repository.sql_cuenta_repository import SqlCuentaRepository


router = APIRouter(
    prefix="/programacion-ahorro",
    tags=["ProgramacionAhorro"],
    dependencies=[Depends(get_current_user)],
)


def get_programacion_repository(
    db: Session = Depends(get_db),
) -> ProgramacionAhorroRepository:
    return SqlProgramacionRepository(db)


def get_cuenta_repository(
    db: Session = Depends(get_db),
) -> CuentaRepository:
    return SqlCuentaRepository(db)


@router.post("/", response_model=ProgramacionResponse, status_code=201)
def crear_programacion(
    programacion: ProgramacionCreate,
    current_user: object = Depends(get_current_user),
    repository: ProgramacionAhorroRepository = Depends(get_programacion_repository),
    cuenta_repository: CuentaRepository = Depends(get_cuenta_repository),
):
    caso_uso = CrearProgramacion(repository, cuenta_repository)
    return caso_uso.execute(programacion.model_dump(), current_user.id_usuario)