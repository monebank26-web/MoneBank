from pydantic import BaseModel, EmailStr, field_validator

from app.core.security.password_policy import validate_password


class PasswordRecoveryRequest(BaseModel):
    correo: EmailStr


class PasswordRecoveryConfirmRequest(BaseModel):
    token: str
    nueva_contrasena: str

    @field_validator("nueva_contrasena")
    @classmethod
    def validar_contrasena(cls, value):
        return validate_password(value)
