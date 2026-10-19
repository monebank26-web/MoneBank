from fastapi import APIRouter, Depends, HTTPException
from fastapi.background import BackgroundTasks

from app.core.security.auth import get_current_user
from app.core.database.unit_of_work import UnitOfWork
from app.core.dependencies.email_service import EmailService
from app.core.dependencies.repositories import get_unit_of_work

from app.modules.auth.application.use_cases.login_usuario import LoginUsuarioUseCase
from app.modules.auth.application.use_cases.request_password_recovery import RequestPasswordRecoveryUseCase
from app.modules.auth.application.use_cases.confirm_password_recovery import ConfirmPasswordRecoveryUseCase
from app.modules.auth.application.use_cases.actualizar_contrasena import ActualizarContrasenaUseCase

from app.modules.auth.presentation.schema.change_password_request import ContrasenaUpdateRequest
from app.modules.auth.presentation.schema.login_request import LoginRequest
from app.modules.auth.presentation.schema.login_response import LoginResponse
from app.modules.auth.presentation.schema.password_recovery_request import ( PasswordRecoveryRequest, PasswordRecoveryConfirmRequest)
from app.modules.auth.presentation.schema.password_recovery_response import PasswordRecoveryResponse


from app.shared.exceptions.auth_errors import (
    AccountLockedException,
    EmailNotFoundException,
    InvalidCredentialsException,
    InvalidOrExpiredTokenException,
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


def get_email_service() -> EmailService:
    return EmailService()


@router.post(
    "/login",
    response_model=LoginResponse,
    summary="Iniciar sesión",
    description="Autentica un usuario mediante correo y contraseña.",
    responses = {
        200: {"description": "Login exitoso, devuelve token JWT"},
        401: {"description": "Credenciales incorrectas"},
        423: {"description": "Cuenta bloqueada temporalmente por múltiples intentos fallidos"},
        422: {"description": "Datos de entrada inválidos"},
        500: {"description": "Error interno del servidor"},
    }
)
def login(
    request: LoginRequest,
    unit_of_work: UnitOfWork = Depends(get_unit_of_work),
):
    use_case = LoginUsuarioUseCase(unit_of_work.auth)
    resultado = use_case.execute(request.correo, request.contrasena)
    unit_of_work.commit()
    return resultado


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
        404: {"description": "El correo no está registrado"},
        422: {"description": "Datos de entrada inválidos"},
        500: {"description": "Error interno del servidor"},
    }
)
def request_password_recovery(
    request: PasswordRecoveryRequest,
    background_tasks: BackgroundTasks,
    unit_of_work: UnitOfWork = Depends(get_unit_of_work),
    email_service: EmailService = Depends(get_email_service),
):
    use_case = RequestPasswordRecoveryUseCase(
        unit_of_work.auth, unit_of_work.usuarios, email_service
    )
    result = use_case.execute(request.correo)
    unit_of_work.commit()
    return result

@router.post(
    "/cambiar-password",
    response_model=PasswordRecoveryResponse,
    summary="Cambiar contraseña",
)
def cambiar_contrasena(
    request: ContrasenaUpdateRequest,
    unit_of_work: UnitOfWork = Depends(get_unit_of_work),
    current_user: object = Depends(get_current_user),
):
    caso_uso = ActualizarContrasenaUseCase(unit_of_work.usuarios)
    resultado = caso_uso.execute(
        current_user.id_usuario,
        request.contrasena_actual,
        request.contrasena_nueva
    )
    unit_of_work.commit()
    return resultado


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
        410: {"description": "El token es inválido o ha expirado"},
        422: {"description": "Datos de entrada inválidos"},
        500: {"description": "Error interno del servidor"},
    }
)
def confirm_password_recovery(
    request: PasswordRecoveryConfirmRequest,
    unit_of_work: UnitOfWork = Depends(get_unit_of_work),
):
    use_case = ConfirmPasswordRecoveryUseCase(unit_of_work.auth, unit_of_work.usuarios)
    resultado = use_case.execute(request.token, request.nueva_contrasena)
    unit_of_work.commit()
    return resultado
