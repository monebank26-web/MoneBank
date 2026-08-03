from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database.connection import get_db


router = APIRouter(
    prefix="/transacciones",
    tags=["transacciones"]
)


@router.post("/", response_model=transaccionResponse)
def registrar_movimiento(
    transaccion: transaccionCreate,
    db: Session = Depends(get_db)
):

    caso_uso = CrearUsuario()

    return caso_uso.execute(
        db,
        usuario.model_dump()
    )