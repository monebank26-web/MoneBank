from fastapi import APIRouter, Depends, HTTPException
from Backend.app.modules.transaccion.presentation.schema.trans_schema import ListaTransaccionesResponse
from sqlalchemy.orm import Session

from app.core.database.connection import get_db

from typing import List


router = APIRouter(
    prefix="/transacciones",
    tags=["transacciones"]
)

@router.get(
    "/",
    response_model=List[ListaTransaccionesResponse],
    status_code=200
)
def obtener_Transacciones(
    db: Session = Depends(get_db)
):
    caso_uso = ObtenerTransaccionesUseCase(
        SqlTransaccionesRepository()
    )

    try:
        return caso_uso.execute(db)
    except TransaccionesNoEncontrado:
        raise HTTPException(
            status_code=404,
            detail=" no encontrado"
        )