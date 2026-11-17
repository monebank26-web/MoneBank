from pydantic import BaseModel, EmailStr, Field


class PasswordRecoveryRequest(BaseModel):
    correo: EmailStr


class PasswordRecoveryConfirmRequest(BaseModel):
    correo: EmailStr
    codigo: str = Field(..., pattern=r"^\d{6}$")
    nueva_contrasena: str
