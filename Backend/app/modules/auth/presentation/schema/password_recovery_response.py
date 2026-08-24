from pydantic import BaseModel


class PasswordRecoveryResponse(BaseModel):
    mensaje: str
