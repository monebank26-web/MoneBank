from fastapi import APIRouter, Depends

from app.core.dependencies.database import get_db
from app.modules.auth.application.use_cases.login_usuario import LoginUsuarioUseCase
from app.modules.auth.presentation.schema.login_request import LoginRequest
from app.modules.auth.presentation.schema.login_response import LoginResponse

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/login", response_model=LoginResponse)
def login(
    request: LoginRequest,
    db=Depends(get_db),
    use_case: LoginUsuarioUseCase = Depends()
):
    return use_case.execute(db, request.correo, request.contrasena)