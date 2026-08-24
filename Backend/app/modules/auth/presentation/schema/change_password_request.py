from pydantic import BaseModel, field_validator
from app.core.security.password_policy import validate_password


class ContrasenaUpdateRequest(BaseModel):
    contrasena_actual: str
    contrasena_nueva: str
    

    @field_validator("contrasena_nueva")
    @classmethod
    def validar_contrasena_nueva(cls, value):
        return validate_password(value)
