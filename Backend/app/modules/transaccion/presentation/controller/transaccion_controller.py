from fastapi import Depends

from app.core.database.unit_of_work import UnitOfWork
from app.core.dependencies.repositories import get_unit_of_work
from app.modules.transaccion.application.use_cases.actualizar_transaccion import (
    ActualizarTransaccion,
)
from app.modules.transaccion.application.use_cases.obtener_categorias import (
    ObtenerCategoriasUseCase,
)
from app.modules.transaccion.application.use_cases.obtener_detalle_transaccion import (
    ObtenerDetalleUseCase,
)
from app.modules.transaccion.application.use_cases.obtener_transacciones_historial import (
    ObtenerHistorialUseCase,
)
from app.modules.transaccion.application.use_cases.registrar_abono_ahorro import (
    RegistrarAbonoAhorro,
)
from app.modules.transaccion.application.use_cases.registrar_gasto import RegistrarGasto
from app.modules.transaccion.application.use_cases.registrar_ingreso import RegistrarIngreso
from app.modules.transaccion.domain.interface.trans_repository import (
    TransaccionRepository,
)
from app.modules.transaccion.presentation.schema.trans_schema import (
    AbonoAhorroRequest,
    CategoriaResponse,
    GastoRequest,
    HistorialRequest,
    TransaccionUpdateRequest,
)


class TransaccionController:

    def __init__(
        self,
        repository: TransaccionRepository,
        unit_of_work: UnitOfWork,
    ):
        self.repository = repository
        self.unit_of_work = unit_of_work

    def registrar_gasto(self, gasto: GastoRequest, current_user):
        resultado = RegistrarGasto(self.repository).execute(
            gasto.model_dump(),
            current_user.id_usuario,
        )
        self.unit_of_work.commit()
        return resultado

    def registrar_ingreso(self, ingreso: GastoRequest, current_user):
        resultado = RegistrarIngreso(self.repository).execute(
            ingreso.model_dump(),
            current_user.id_usuario,
        )
        self.unit_of_work.commit()
        return resultado

    def registrar_abono_ahorro(self, abono: AbonoAhorroRequest, current_user):
        resultado = RegistrarAbonoAhorro(self.repository).execute(
            abono.model_dump(),
            current_user.id_usuario,
        )
        self.unit_of_work.commit()
        return resultado

    def obtener_historial(self, current_user, filtros: HistorialRequest):
        return ObtenerHistorialUseCase(self.repository).execute(
            current_user.id_usuario,
            filtros.model_dump(),
        )

    def obtener_categorias(self, current_user) -> list[CategoriaResponse]:
        return ObtenerCategoriasUseCase(self.repository).execute()

    def obtener_detalle(self, id_transaccion: int, current_user):
        return ObtenerDetalleUseCase(self.repository).execute(
            current_user.id_usuario,
            id_transaccion,
        )

    def actualizar_transaccion(
        self,
        id_transaccion: int,
        transaccion: TransaccionUpdateRequest,
        current_user,
    ):
        resultado = ActualizarTransaccion(self.repository).execute(
            id_transaccion,
            transaccion.model_dump(),
            current_user.id_usuario,
        )
        self.unit_of_work.commit()
        return resultado


def get_transaccion_controller(
    unit_of_work: UnitOfWork = Depends(get_unit_of_work),
) -> TransaccionController:
    return TransaccionController(unit_of_work.transacciones, unit_of_work)
