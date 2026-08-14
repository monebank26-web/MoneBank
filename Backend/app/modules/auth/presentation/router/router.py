from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies.database import get_db
from app.modules.auth.application.use_cases.login_usuario import LoginUsuarioUseCase
from app.modules.auth.domain.interface.auth_repository import AuthRepository
from app.modules.auth.infrastructure.repository.sql_auth_repository import SqlAuthRepository
from app.modules.auth.presentation.schema.login_request import LoginRequest
from app.modules.auth.presentation.schema.login_response import LoginResponse

from app.shared.exceptions.business_exceptions import InvalidCredentialsException, AccountLockedException
from app.shared.exceptions.http_exceptions import ValidationException, InternalServerException


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


def get_auth_repository(
    db: Session = Depends(get_db)
) -> AuthRepository:
    return SqlAuthRepository(db)


@router.post(
    "/login",
    response_model=LoginResponse,
    summary="Iniciar sesión",
    description="Autentica un usuario mediante correo y contraseña.",
    responses = {
    200: {"description": "Login exitoso, devuelve token JWT"},
    InvalidCredentialsException.status_code: {"description": InvalidCredentialsException.description},
    AccountLockedException.status_code: {"description": AccountLockedException.description},
    ValidationException.status_code: {"description": ValidationException.description},
    InternalServerException.status_code: {"description": InternalServerException.description},
}
)
def login(
    request: LoginRequest,
    repository: AuthRepository = Depends(get_auth_repository)
):
    use_case = LoginUsuarioUseCase(repository)
    return use_case.execute(request.correo, request.contrasena)
