from  pydantic import BaseModel

class ListaTransaccionesResponse(BaseModel):

    id: int
    tipo: str
    monto: Decimal
    fecha: date
    categoria: str
    descripcion: str

    model_config = ConfigDict(
        from_attributes=True
    )