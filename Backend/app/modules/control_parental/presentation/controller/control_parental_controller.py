from fastapi import Depends, HTTPException

from app.core.database.unit_of_work import UnitOfWork
from app.core.dependencies.email_service import EmailService
from app.core.dependencies.repositories import get_unit_of_work
from app.modules.control_parental.application.use_cases.confirmar_desvinculacion import (
    ConfirmarDesvinculacionUseCase,
)
from app.modules.control_parental.application.use_cases.confirmar_vinculacion import (
    ConfirmarVinculacionUseCase,
)
from app.modules.control_parental.application.use_cases.dashboard_parental import (
    ActualizarPermisosHijo,
    ListarHijosParentales,
    ObtenerPermisosHijo,
    ObtenerResumenHijo,
    ObtenerTransaccionesHijo,
)
from app.modules.control_parental.application.use_cases.obtener_vinculaciones import (
    ObtenerVinculacionesUseCase,
)
from app.modules.control_parental.application.use_cases.solicitar_desvinculacion import (
    SolicitarDesvinculacionUseCase,
)
from app.modules.control_parental.application.use_cases.solicitar_vinculacion import (
    SolicitarVinculacionUseCase,
)
from app.modules.control_parental.domain.interface.control_parental_repository import (
    ControlParentalRepository,
)
from app.modules.control_parental.presentation.schema.control_parental_schema import (
    ConfirmarCodigoRequest,
    PermisosUpdate,
    SolicitarDesvinculacionRequest,
    SolicitarVinculacionRequest,
    SolicitudResponse,
)


def get_email_service():
    return EmailService()


def manejar_error(error):
    status_code = getattr(error, "status_code", 403)

    detail = getattr(
        error,
        "message",
        str(error),
    )

    raise HTTPException(
        status_code=status_code,
        detail=detail,
    )


class ControlParentalController:

    def __init__(
        self,
        repository: ControlParentalRepository,
        unit_of_work: UnitOfWork,
        email_service: EmailService,
    ):
        self.repository = repository
        self.unit_of_work = unit_of_work
        self.email_service = email_service

    def solicitar_vinculacion(
        self,
        data: SolicitarVinculacionRequest,
        current_user,
    ):
        caso_uso = SolicitarVinculacionUseCase(
            repository=self.unit_of_work.parentales,
            email_service=self.email_service,
        )

        resultado = caso_uso.execute(
            id_padre=current_user.id_usuario,
            nombre_hijo=data.nombre_hijo,
            correo_hijo=data.correo_hijo,
        )
        self.unit_of_work.commit()
        return resultado

    def confirmar_vinculacion(
        self,
        data: ConfirmarCodigoRequest,
        current_user,
    ):
        caso_uso = ConfirmarVinculacionUseCase(self.unit_of_work.parentales)

        resultado = caso_uso.execute(
            current_user.id_usuario,
            data.codigo,
        )
        self.unit_of_work.commit()
        return resultado

    def obtener_vinculaciones(self, current_user):
        return ObtenerVinculacionesUseCase(
            self.repository
        ).execute(
            current_user.id_usuario
        )

    def solicitar_desvinculacion(
        self,
        data: SolicitarDesvinculacionRequest,
        current_user,
    ):
        solicitud = SolicitarDesvinculacionUseCase(
            self.unit_of_work.parentales,
            self.email_service,
        ).execute(
            current_user.id_usuario,
            data.correo_padre,
        )
        self.unit_of_work.commit()

        return SolicitudResponse(
            mensaje="Código enviado al correo del padre",
            id_solicitud=solicitud.id_solicitud,
        )

    def confirmar_desvinculacion(
        self,
        data: ConfirmarCodigoRequest,
        current_user,
    ):
        ConfirmarDesvinculacionUseCase(
            self.unit_of_work.parentales
        ).execute(
            current_user.id_usuario,
            data.codigo,
        )
        self.unit_of_work.commit()

        return {
            "mensaje": "Cuenta desvinculada correctamente"
        }

    def listar_hijos(self, current_user):
        try:
            return ListarHijosParentales(
                self.repository
            ).execute(
                current_user.id_usuario
            )
        except Exception as error:
            manejar_error(error)

    def obtener_resumen_hijo(self, id_hijo: int, current_user):
        try:
            return ObtenerResumenHijo(
                self.repository
            ).execute(
                current_user.id_usuario,
                id_hijo,
            )
        except Exception as error:
            manejar_error(error)

    def obtener_transacciones_hijo(
        self,
        id_hijo: int,
        limite: int,
        current_user,
    ):
        try:
            return ObtenerTransaccionesHijo(
                self.repository
            ).execute(
                current_user.id_usuario,
                id_hijo,
                limite,
            )
        except Exception as error:
            manejar_error(error)

    def obtener_permisos_hijo(self, id_hijo: int, current_user):
        try:
            return ObtenerPermisosHijo(
                self.repository
            ).execute(
                current_user.id_usuario,
                id_hijo,
            )
        except Exception as error:
            manejar_error(error)

    def actualizar_permisos_hijo(
        self,
        id_hijo: int,
        data: PermisosUpdate,
        current_user,
    ):
        try:
            resultado = ActualizarPermisosHijo(
                self.unit_of_work.parentales
            ).execute(
                current_user.id_usuario,
                id_hijo,
                data.permisos,
            )
            self.unit_of_work.commit()
            return resultado
        except Exception as error:
            manejar_error(error)


def get_control_parental_controller(
    unit_of_work: UnitOfWork = Depends(get_unit_of_work),
    email_service: EmailService = Depends(get_email_service),
) -> ControlParentalController:
    return ControlParentalController(
        unit_of_work.parentales,
        unit_of_work,
        email_service,
    )
