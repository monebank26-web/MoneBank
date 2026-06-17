from pydantic import BaseModel


class UsuarioCreate(BaseModel):
    nombres: str
    apellidos: str
    correo: str
    contrasena: str
    estado: str
    id_rol: int
    id_tipo_usuario: int


class UsuarioResponse(BaseModel):
    id_usuario: int
    nombres: str
    apellidos: str
    correo: str

    class Config:
        from_attributes = True