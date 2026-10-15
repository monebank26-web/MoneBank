from fastapi import Depends

from app.core.database.unit_of_work import UnitOfWork
from app.core.dependencies.repositories import get_unit_of_work
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

    def __init__(
        self,
        repository: CuentaRepository,
        unit_of_work: UnitOfWork,
    ):
        self.repository = repository
        self.unit_of_work = unit_of_work

    @staticmethod
    def _es_admin(current_user) -> bool:
        return current_user.id_rol == ROL_ADMIN

    def crear_cuenta(self, cuenta: CuentaCreate):
        resultado = CrearCuenta(self.repository).execute(cuenta.model_dump())
        self.unit_of_work.commit()
        return resultado

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
        resultado = ActualizarCuentaUseCase(self.repository).execute(
            id_cuenta,
            cuenta.model_dump(exclude_unset=True),
            current_user.id_usuario,
            self._es_admin(current_user),
        )
        self.unit_of_work.commit()
        return resultado

    def eliminar_cuenta(self, id_cuenta: int, current_user):
        resultado = EliminarCuentaUseCase(self.repository).execute(
            id_cuenta,
            current_user.id_usuario,
            self._es_admin(current_user),
        )
        self.unit_of_work.commit()
        return resultado


def get_cuenta_controller(
    unit_of_work: UnitOfWork = Depends(get_unit_of_work),
) -> CuentaController:
    return CuentaController(unit_of_work.cuentas, unit_of_work)
