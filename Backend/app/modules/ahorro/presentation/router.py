from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database.connection import get_db

from app.modules.ahorro.infrastucture.repository.sql_ahorro_repository import (
    SqlAhorroRepository
)

from app.modules.ahorro.application.use_cases.crear_ahorro import (
    CrearAhorro
)

from app.modules.ahorro.application.use_cases.obtener_ahorro import (
    ObtenerAhorrosUseCase
)

from app.modules.ahorro.application.use_cases.obtener_ahorro_por_id import (
    ObtenerAhorroPorIdUseCase
)

from app.modules.ahorro.application.use_cases.actualizar_ahorro import (
    ActualizarAhorroUseCase
)

from app.modules.ahorro.application.use_cases.eliminar_ahorro import (
    EliminarAhorroUseCase
)

from app.modules.ahorro.presentation.schema.ahorro_schema import (
    AhorroCreate,
    AhorroResponse
)

router = APIRouter(
    prefix="/ahorros",
    tags=["Ahorros"]
)


@router.post("/", response_model=AhorroResponse)
def crear_ahorro(
    ahorro: AhorroCreate,
    db: Session = Depends(get_db)
):

    caso_uso = CrearAhorro()

    return caso_uso.execute(
        db,
        ahorro.model_dump()
    )


@router.get("/")
def obtener_ahorros(
    db: Session = Depends(get_db)
):

    caso_uso = ObtenerAhorrosUseCase(
        SqlAhorroRepository()
    )

    return caso_uso.execute(db)


@router.get("/{id_ahorro}")
def obtener_ahorro_por_id(
    id_ahorro: int,
    db: Session = Depends(get_db)
):

    caso_uso = ObtenerAhorroPorIdUseCase(
        SqlAhorroRepository()
    )

    return caso_uso.execute(
        db,
        id_ahorro
    )


@router.put("/{id_ahorro}")
def actualizar_ahorro(
    id_ahorro: int,
    ahorro: AhorroCreate,
    db: Session = Depends(get_db)
):

    caso_uso = ActualizarAhorroUseCase(
        SqlAhorroRepository()
    )

    return caso_uso.execute(
        db,
        id_ahorro,
        ahorro.model_dump()
    )


@router.delete("/{id_ahorro}")
def eliminar_ahorro(
    id_ahorro: int,
    db: Session = Depends(get_db)
):

    caso_uso = EliminarAhorroUseCase(
        SqlAhorroRepository()
    )

    return caso_uso.execute(
        db,
        id_ahorro
    )