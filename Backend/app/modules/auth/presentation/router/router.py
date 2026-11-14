from fastapi import APIRouter, Depends

from app.core.security.auth import get_current_user

from app.modules.auth.presentation.controller.auth_controller import (
    AuthController,
    get_auth_controller,
    get_email_service,
)
from app.modules.auth.presentation.schema.change_password_request import (
    ContrasenaUpdateRequest,
)
from app.modules.auth.presentation.schema.login_request import LoginRequest
from app.modules.auth.presentation.schema.login_response import LoginResponse
from app.modules.auth.presentation.schema.password_recovery_request import (
    PasswordRecoveryConfirmRequest,
    PasswordRecoveryRequest,
)
from app.modules.auth.presentation.schema.password_recovery_response import (
    PasswordRecoveryResponse,
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


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
    controller: AuthController = Depends(get_auth_controller),
):
    return controller.login(request)


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
    controller: AuthController = Depends(get_auth_controller),
):
    return controller.request_password_recovery(request)


@router.post(
    "/cambiar-password",
    response_model=PasswordRecoveryResponse,
    summary="Cambiar contraseña",
)
def cambiar_contrasena(
    request: ContrasenaUpdateRequest,
    current_user: object = Depends(get_current_user),
    controller: AuthController = Depends(get_auth_controller),
):
    return controller.cambiar_contrasena(request, current_user)


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
    },
)
def confirm_password_recovery(
    request: PasswordRecoveryConfirmRequest,
    controller: AuthController = Depends(get_auth_controller),
):
    return controller.confirm_password_recovery(request)
