from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security.auth import get_usuario_repository, get_current_user
from app.core.database.connection import get_db

from app.modules.auth.application.use_cases.login_usuario import LoginUsuarioUseCase
from app.modules.auth.application.use_cases.request_password_recovery import RequestPasswordRecoveryUseCase
from app.modules.auth.application.use_cases.confirm_password_recovery import ConfirmPasswordRecoveryUseCase
from app.modules.auth.application.use_cases.actualizar_contrasena import ActualizarContrasenaUseCase

from app.modules.auth.domain.interface.auth_repository import AuthRepository
from app.modules.auth.infrastructure.repository.sql_auth_repository import SqlAuthRepository


from app.shared.exceptions.business_exceptions import (InvalidCredentialsException, AccountLockedException,EmailNotFoundException, InvalidOrExpiredTokenException)
from app.shared.exceptions.http_exceptions import ValidationException, InternalServerException


router = APIRouter(
    prefix="/ProgramacionAhorro",
    tags=["ProgramacionAhorro"]
)


def get_auth_repository(
    db: Session = Depends(get_db),
    programacion_repository: ProgramacionRepository = Depends(get_usuario_repository)
) -> AuthRepository:
    return SqlProgramacionRepository(db, programacion_repository)


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
