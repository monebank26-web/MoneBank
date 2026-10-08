from fastapi import Depends

from app.core.dependencies.repositories import get_cuenta_repository
from app.core.security.roles import ROL_ADMIN
from app.modules.cuenta.application.use_cases.actualizar_cuenta import (
    ActualizarCuentaUseCase,
)
from app.modules.cuenta.application.use_cases.crear_cuenta import CrearCuenta
from app.modules.cuenta.application.use_cases.eliminar_cuenta import (
    EliminarCuentaUseCase,
)
from app.modules.cuenta.application.use_cases.obtener_cuenta import (
    ObtenerCuentasUseCase,
)
from app.modules.cuenta.application.use_cases.obtener_cuenta_por_id_cuenta import (
    ObtenerCuentaPorIdUseCase,
)
from app.modules.cuenta.application.use_cases.obtener_cuenta_por_usuario import (
    ObtenerCuentaPorUsuarioUseCase,
)
from app.modules.cuenta.domain.interface.cuenta_repository import CuentaRepository
from app.modules.cuenta.presentation.schema.cuenta_schema import (
    CuentaCreate,
    CuentaUpdate,
)


class CuentaController:

    def __init__(self, repository: CuentaRepository):
        self.repository = repository

    @staticmethod
    def _es_admin(current_user) -> bool:
        return current_user.id_rol == ROL_ADMIN

    def crear_cuenta(self, cuenta: CuentaCreate):
        return CrearCuenta(self.repository).execute(cuenta.model_dump())

    def obtener_cuentas(self, current_user, usuario_id=None):
        if self._es_admin(current_user):
            if usuario_id:
                caso_uso = ObtenerCuentaPorUsuarioUseCase(self.repository)
                return [caso_uso.execute(usuario_id)]
            return ObtenerCuentasUseCase(self.repository).execute()

        caso_uso = ObtenerCuentaPorUsuarioUseCase(self.repository)
        return [caso_uso.execute(current_user.id_usuario)]

    def obtener_cuenta_por_id(self, id_cuenta: int, current_user):
        return ObtenerCuentaPorIdUseCase(self.repository).execute(
            id_cuenta,
            current_user.id_usuario,
            self._es_admin(current_user),
        )

    def actualizar_cuenta(
        self,
        id_cuenta: int,
        cuenta: CuentaUpdate,
        current_user,
    ):
        return ActualizarCuentaUseCase(self.repository).execute(
            id_cuenta,
            cuenta.model_dump(exclude_unset=True),
            current_user.id_usuario,
            self._es_admin(current_user),
        )

    def eliminar_cuenta(self, id_cuenta: int, current_user):
        return EliminarCuentaUseCase(self.repository).execute(
            id_cuenta,
            current_user.id_usuario,
            self._es_admin(current_user),
        )


def get_cuenta_controller(
    repository: CuentaRepository = Depends(get_cuenta_repository),
) -> CuentaController:
    return CuentaController(repository)
