from pydantic import BaseModel


class ConsejoResponse(BaseModel):
    id_transaccion: int
    consejo: str
    generado_con_ia: bool
