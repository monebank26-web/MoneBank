from datetime import date
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field, field_validator

from app.core.security.password_policy import validate_password
from app.shared.constants.motivo_bloqueo import DESCRIPCION_MOTIVO_BLOQUEO


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
    estado: str
    id_rol: Optional[int] = None
    fecha_creacion: date

    class Config:
        from_attributes = True


class UsuarioListResponse(BaseModel):
    items: List[UsuarioResponse]
    total: int
    pagina: int
    por_pagina: int


class UsuarioDesactivadoResponse(BaseModel):
    mensaje: str


class BloqueoUsuarioRequest(BaseModel):
    motivo: Optional[str] = Field(
        None,
        max_length=255,
        description=DESCRIPCION_MOTIVO_BLOQUEO,
    )

    @field_validator("motivo", mode="before")
    @classmethod
    def limpiar_motivo(cls, value):
        return value.strip() if isinstance(value, str) else value


class BloqueoUsuarioResponse(BaseModel):
    id_usuario: int
    estado: str
    motivo_bloqueo: str
    fecha_bloqueo: datetime

    class Config:
        from_attributes = True
