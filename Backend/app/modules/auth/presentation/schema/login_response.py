from pydantic import BaseModel
from typing import Optional


class UsuarioLoginData(BaseModel):
    id_usuario: int
    nombres: str
    apellidos: str
    correo: str
    estado: str
    id_rol: int
    id_tipo_usuario: int


class LoginResponse(BaseModel):
    success: bool
    message: Optional[str] = None
    token: Optional[str] = None
    usuario: Optional[UsuarioLoginData] = None