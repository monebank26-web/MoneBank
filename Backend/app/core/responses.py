from typing import Any, Optional

from pydantic import BaseModel


class SuccessResponse(BaseModel):
    success: bool = True
    message: str = "Operación exitosa"
    data: Optional[Any] = None


class ErrorResponse(BaseModel):
    success: bool = False
    message: str
