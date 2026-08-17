from fastapi import APIRouter, Depends
from fastapi.background import BackgroundTasks
from sqlalchemy.orm import Session

from app.core.database.connection import get_db
from app.core.dependencies.email_service import EmailService
from app.modules.auth.application.use_cases.login_usuario import LoginUsuarioUseCase
from app.modules.auth.application.use_cases.request_password_recovery import RequestPasswordRecoveryUseCase
from app.modules.auth.application.use_cases.confirm_password_recovery import ConfirmPasswordRecoveryUseCase
from app.modules.auth.domain.interface.auth_repository import AuthRepository
from app.modules.auth.infrastructure.repository.sql_auth_repository import SqlAuthRepository
from app.modules.auth.presentation.schema.login_request import LoginRequest
from app.modules.auth.presentation.schema.login_response import LoginResponse
from app.modules.auth.presentation.schema.password_recovery_request import ( PasswordRecoveryRequest, PasswordRecoveryConfirmRequest)
from app.modules.auth.presentation.schema.password_recovery_response import PasswordRecoveryResponse
from app.modules.usuario.domain.interface.usuario_repository import UsuarioRepository
from app.modules.usuario.presentation.router.router import get_usuario_repository

from app.shared.exceptions.business_exceptions import (InvalidCredentialsException, AccountLockedException,EmailNotFoundException, InvalidOrExpiredTokenException)
from app.shared.exceptions.http_exceptions import ValidationException, InternalServerException


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


def get_auth_repository(
    db: Session = Depends(get_db),
    usuario_repository: UsuarioRepository = Depends(get_usuario_repository)
) -> AuthRepository:
    return SqlAuthRepository(db, usuario_repository)


def get_email_service() -> EmailService:
    return EmailService()


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


@router.post(
    "/password-recovery/request",
    response_model=PasswordRecoveryResponse,
    summary="Solicitar recuperación de contraseña",
    description=(
        "Envía un enlace de recuperación al correo registrado. "
        "Si el correo no está registrado, no se revela esa información."
    ),
    responses={
        200: {"description": "Solicitud procesada (mensaje genérico)"},
        EmailNotFoundException.status_code: {"description": EmailNotFoundException.description},
        ValidationException.status_code: {"description": ValidationException.description},
        InternalServerException.status_code: {"description": InternalServerException.description},
    }
)
def request_password_recovery(
    request: PasswordRecoveryRequest,
    background_tasks: BackgroundTasks,
    repository: AuthRepository = Depends(get_auth_repository),
    usuario_repository: UsuarioRepository = Depends(get_usuario_repository),
    email_service: EmailService = Depends(get_email_service),
):
    use_case = RequestPasswordRecoveryUseCase(
        repository, usuario_repository, email_service
    )
    result = use_case.execute(request.correo)
    return result


@router.post(
    "/password-recovery/confirm",
    response_model=PasswordRecoveryResponse,
    summary="Confirmar recuperación de contraseña",
    description=(
        "Establece una nueva contraseña usando el token de recuperación "
        "recibido por correo."
    ),
    responses={
        200: {"description": "Contraseña restablecida exitosamente"},
        InvalidOrExpiredTokenException.status_code: {"description": InvalidOrExpiredTokenException.description},
        ValidationException.status_code: {"description": ValidationException.description},
        InternalServerException.status_code: {"description": InternalServerException.description},
    }
)
def confirm_password_recovery(
    request: PasswordRecoveryConfirmRequest,
    repository: AuthRepository = Depends(get_auth_repository),
    usuario_repository: UsuarioRepository = Depends(get_usuario_repository),
):
    use_case = ConfirmPasswordRecoveryUseCase(repository, usuario_repository)
    return use_case.execute(request.token, request.nueva_contrasena)
