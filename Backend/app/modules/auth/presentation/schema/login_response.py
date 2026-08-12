from pydantic import BaseModel


class UsuarioLoginData(BaseModel):
    id_usuario: int
    nombres: str
    apellidos: str
    correo: str
    estado: str
    id_rol: int
    id_tipo_usuario: int


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    usuario_id: int