from typing import Optional

from pydantic import BaseModel, EmailStr, field_validator

from app.core.security.password_policy import validate_password


class UsuarioCreate(BaseModel):
    nombres: str
    apellidos: str
    correo: EmailStr
    contrasena: str

    @field_validator("contrasena")
    @classmethod
    def validar_contrasena(cls, value):
        return validate_password(value)


class UsuarioUpdate(BaseModel):
    nombres: Optional[str] = None
    apellidos: Optional[str] = None
    correo: Optional[EmailStr] = None


class UsuarioResponse(BaseModel):
    id_usuario: int
    nombres: str
    apellidos: str
    correo: EmailStr

    class Config:
        from_attributes = True