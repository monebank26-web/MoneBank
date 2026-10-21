from fastapi import Depends

from app.core.database.unit_of_work import UnitOfWork
from app.core.dependencies.email_service import EmailService
from app.core.dependencies.repositories import get_unit_of_work
from app.modules.auth.application.use_cases.actualizar_contrasena import (
    ActualizarContrasenaUseCase,
)
from app.modules.auth.application.use_cases.confirm_password_recovery import (
    ConfirmPasswordRecoveryUseCase,
)
from app.modules.auth.application.use_cases.login_usuario import LoginUsuarioUseCase
from app.modules.auth.application.use_cases.request_password_recovery import (
    RequestPasswordRecoveryUseCase,
)
from app.modules.auth.domain.interface.auth_repository import AuthRepository
from app.modules.auth.presentation.schema.change_password_request import (
    ContrasenaUpdateRequest,
)
from app.modules.auth.presentation.schema.login_request import LoginRequest
from app.modules.auth.presentation.schema.password_recovery_request import (
    PasswordRecoveryConfirmRequest,
    PasswordRecoveryRequest,
)


def get_email_service() -> EmailService:
    return EmailService()


class AuthController:

    def __init__(
        self,
        repository: AuthRepository,
        unit_of_work: UnitOfWork,
        email_service: EmailService,
    ):
        self.repository = repository
        self.unit_of_work = unit_of_work
        self.email_service = email_service

    def login(self, request: LoginRequest):
        caso_uso = LoginUsuarioUseCase(self.repository)
        resultado = caso_uso.execute(request.correo, request.contrasena)
        self.unit_of_work.commit()
        return resultado

    def request_password_recovery(self, request: PasswordRecoveryRequest):
        caso_uso = RequestPasswordRecoveryUseCase(
            self.repository,
            self.unit_of_work.usuarios,
            self.email_service,
        )
        resultado = caso_uso.execute(request.correo)
        self.unit_of_work.commit()
        return resultado

    def cambiar_contrasena(self, request: ContrasenaUpdateRequest, current_user):
        caso_uso = ActualizarContrasenaUseCase(self.unit_of_work.usuarios)
        resultado = caso_uso.execute(
            current_user.id_usuario,
            request.contrasena_actual,
            request.contrasena_nueva,
        )
        self.unit_of_work.commit()
        return resultado

    def confirm_password_recovery(self, request: PasswordRecoveryConfirmRequest):
        caso_uso = ConfirmPasswordRecoveryUseCase(
            self.repository,
            self.unit_of_work.usuarios,
        )
        resultado = caso_uso.execute(request.token, request.nueva_contrasena)
        self.unit_of_work.commit()
        return resultado


def get_auth_controller(
    unit_of_work: UnitOfWork = Depends(get_unit_of_work),
    email_service: EmailService = Depends(get_email_service),
) -> AuthController:
    return AuthController(unit_of_work.auth, unit_of_work, email_service)
