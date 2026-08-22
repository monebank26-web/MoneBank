from pydantic import BaseModel


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    usuario_id: int
    id_rol: int
    nombres: str
    apellidos: str
    correo: str