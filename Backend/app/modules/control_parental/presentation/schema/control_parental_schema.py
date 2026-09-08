from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional, Dict , List
from decimal import Decimal
from datetime import datetime
class SolicitarVinculacionRequest(BaseModel):
    correo_hijo: EmailStr
    nombre_hijo: str = Field(..., min_length=1, max_length=100)
class ConfirmarCodigoRequest(BaseModel):
    codigo: str = Field(..., min_length=6, max_length=6, pattern=r"^\d{6}$")
class SolicitarDesvinculacionRequest(BaseModel):
    correo_padre: EmailStr
class RelacionResponse(BaseModel):
    id_control: int
    id_usuario_parental: int
    id_usuario_dependiente: int
    permiso_monitoreo: bool
    estado: str
    model_config = ConfigDict(from_attributes=True)
class SolicitudResponse(BaseModel):
    mensaje: str
    id_solicitud: Optional[int] = None
class HijoParentalResponse(BaseModel):
    id_control: int
    id_usuario: int
    nombres: str
    apellidos: str
    correo: str
    saldo: Decimal
    estado_cuenta: str
    permiso_monitoreo: bool


class PermisoResponse(BaseModel):
    id_permiso: int
    id_control: int
    nombre_permiso: str
    permitido: bool
    model_config = ConfigDict(from_attributes=True)


class PermisosUpdate(BaseModel):
    permisos: Dict[str, bool] = Field(min_length=1)


class ResumenHijoResponse(BaseModel):
    id_control: int
    id_usuario: int
    nombres: str
    apellidos: str
    correo: str
    saldo: Decimal
    estado_cuenta: str
    permisos: Dict[str, bool]


class TransaccionParentalResponse(BaseModel):
    id_transaccion: int
    monto: Decimal
    fecha: datetime
    descripcion: str | None = None
    estado: str
    id_tipo_transaccion: int | None = None
    id_categoria: int | None = None
    model_config = ConfigDict(from_attributes=True)
