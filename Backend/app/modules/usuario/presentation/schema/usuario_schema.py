from datetime import date
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator

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
    fecha_creacion: date

    class Config:
        from_attributes = True


class BloqueoUsuarioRequest(BaseModel):
    motivo: str = Field(..., min_length=5, max_length=255)


class BloqueoUsuarioResponse(BaseModel):
    id_usuario: int
    estado: str
    motivo_bloqueo: str
    fecha_bloqueo: datetime

    class Config:
        from_attributes = True
