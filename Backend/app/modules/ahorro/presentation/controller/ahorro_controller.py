from fastapi import Depends

from app.core.database.unit_of_work import UnitOfWork
from app.core.dependencies.repositories import get_unit_of_work
from app.modules.ahorro.application.use_cases.actualizar_ahorro import (
    ActualizarAhorroUseCase,
)
from app.modules.ahorro.application.use_cases.crear_limite import CrearLimite
from app.modules.ahorro.application.use_cases.crear_meta import CrearMeta
from app.modules.ahorro.application.use_cases.eliminar_ahorro import (
    EliminarAhorroUseCase,
)
from app.modules.ahorro.application.use_cases.obtener_ahorro import (
    ObtenerAhorrosUseCase,
)
from app.modules.ahorro.application.use_cases.obtener_ahorro_por_id import (
    ObtenerAhorroPorIdUseCase,
)
from app.modules.ahorro.application.use_cases.obtener_alertas_presupuesto import (
    ObtenerAlertasPresupuesto,
)
from app.modules.ahorro.application.use_cases.obtener_limites import ObtenerLimites
from app.modules.ahorro.application.use_cases.obtener_metas import ObtenerMetas
from app.modules.ahorro.application.use_cases.obtener_progreso_meta import (
    ObtenerProgresoMeta,
)
from app.modules.ahorro.application.use_cases.obtener_resumen_global_metas import (
    ObtenerResumenGlobalMetas,
)
from app.modules.ahorro.domain.interface.ahorro_repository import AhorroRepository
from app.modules.ahorro.presentation.schema.ahorro_schema import AhorroCreate, MetaCreate
from app.modules.transaccion.application.use_cases.registrar_abono_ahorro import (
    RegistrarAbonoAhorro,
)


class AhorroController:

    def __init__(self, repository: AhorroRepository, unit_of_work: UnitOfWork):
        self.repository = repository
        self.unit_of_work = unit_of_work

    def crear_meta(self, meta: MetaCreate, current_user):
        registrar_abono = RegistrarAbonoAhorro(self.unit_of_work.transacciones)
        caso_uso = CrearMeta(
            self.repository,
            self.unit_of_work.cuentas,
            registrar_abono,
        )
        resultado = caso_uso.execute(meta.model_dump(), current_user.id_usuario)
        self.unit_of_work.commit()
        return resultado

    def obtener_metas(self, current_user):
        return ObtenerMetas(self.repository, self.unit_of_work.cuentas).execute(
            current_user.id_usuario
        )

    def obtener_resumen_global_metas(self, current_user):
        return ObtenerResumenGlobalMetas(
            self.repository,
            self.unit_of_work.cuentas,
        ).execute(current_user.id_usuario)

    def obtener_progreso_meta(self, id_ahorro: int, current_user):
        return ObtenerProgresoMeta(
            self.repository,
            self.unit_of_work.cuentas,
        ).execute(id_ahorro, current_user.id_usuario)

    def crear_limite(self, limite, current_user):
        caso_uso = CrearLimite(self.repository, self.unit_of_work.cuentas)
        resultado = caso_uso.execute(limite.model_dump(), current_user.id_usuario)
        self.unit_of_work.commit()
        return resultado

    def obtener_limites(self, current_user):
        return ObtenerLimites(self.repository, self.unit_of_work.cuentas).execute(
            current_user.id_usuario
        )

    def obtener_alertas_presupuesto(self, current_user):
        return ObtenerAlertasPresupuesto(
            self.repository,
            self.unit_of_work.cuentas,
        ).execute(current_user.id_usuario)

    def obtener_ahorros(self, current_user):
        return ObtenerAhorrosUseCase(
            self.repository,
            self.unit_of_work.cuentas,
        ).execute(current_user.id_usuario)

    def obtener_ahorro_por_id(self, id_ahorro: int, current_user):
        return ObtenerAhorroPorIdUseCase(
            self.repository,
            self.unit_of_work.cuentas,
        ).execute(id_ahorro, current_user.id_usuario)

    def actualizar_ahorro(
        self,
        id_ahorro: int,
        ahorro: AhorroCreate,
        current_user,
    ):
        caso_uso = ActualizarAhorroUseCase(self.repository, self.unit_of_work.cuentas)
        resultado = caso_uso.execute(
            id_ahorro,
            ahorro.model_dump(),
            current_user.id_usuario,
        )
        self.unit_of_work.commit()
        return resultado

    def eliminar_ahorro(self, id_ahorro: int, current_user):
        caso_uso = EliminarAhorroUseCase(self.repository, self.unit_of_work.cuentas)
        resultado = caso_uso.execute(id_ahorro, current_user.id_usuario)
        self.unit_of_work.commit()
        return resultado


def get_ahorro_controller(
    unit_of_work: UnitOfWork = Depends(get_unit_of_work),
) -> AhorroController:
    return AhorroController(unit_of_work.ahorros, unit_of_work)
