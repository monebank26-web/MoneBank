from datetime import date, datetime

from sqlalchemy.orm import Session

from app.modules.control_parental.infrastructure.model.control_parental_model import (
    ControlParentalModel,
    PermisoParentalModel,
)
from app.modules.control_parental.infrastructure.model.ejecucion_mesada_model import (
    EjecucionMesadaModel,
)
from app.modules.control_parental.infrastructure.model.mesada_parental_model import (
    MesadaParentalModel,
)
from app.modules.cuenta.infrastructure.model.cuenta_model import CuentaModel
from app.modules.transaccion.infrastructure.model.categoria_model import (
    CategoriaModel,
)
from app.modules.transaccion.infrastructure.model.tipo_transaccion_model import (
    TipoTransaccionModel,
)
from app.modules.transaccion.infrastructure.model.transaccion_model import (
    TransaccionModel,
)


class SqlEjecucionMesadaRepository:
    def __init__(self, db: Session):
        self.db = db

    def vinculo_activo(self, id_padre: int, id_hijo: int):
        return (
            self.db.query(ControlParentalModel)
            .filter(
                ControlParentalModel.id_usuario_parental == id_padre,
                ControlParentalModel.id_usuario_dependiente == id_hijo,
                ControlParentalModel.estado == "ACTIVO",
            )
            .first()
        )

    def permiso_activo(self, id_control: int):
        permiso = (
            self.db.query(PermisoParentalModel)
            .filter(
                PermisoParentalModel.id_control == id_control,
                PermisoParentalModel.nombre_permiso == "ASIGNAR_MESADA",
            )
            .first()
        )

        return bool(permiso and permiso.permitido)

    def mesada_activa_bloqueada(self, id_control: int):
        return (
            self.db.query(MesadaParentalModel)
            .filter(
                MesadaParentalModel.id_control == id_control,
                MesadaParentalModel.estado == "ACTIVA",
            )
            .with_for_update()
            .first()
        )

    def cuentas_bloqueadas(
        self,
        id_cuenta_padre: int,
        id_cuenta_hijo: int,
    ):
        cuentas = (
            self.db.query(CuentaModel)
            .filter(
                CuentaModel.id_cuenta.in_(
                    [id_cuenta_padre, id_cuenta_hijo]
                )
            )
            .with_for_update()
            .all()
        )

        cuentas_por_id = {
            cuenta.id_cuenta: cuenta
            for cuenta in cuentas
        }

        return (
            cuentas_por_id.get(id_cuenta_padre),
            cuentas_por_id.get(id_cuenta_hijo),
        )

    def ejecucion_periodo(
        self,
        id_mesada: int,
        periodo: str,
    ):
        ejecucion = (
            self.db.query(EjecucionMesadaModel)
            .filter(
                EjecucionMesadaModel.id_mesada == id_mesada,
                EjecucionMesadaModel.periodo == periodo,
                EjecucionMesadaModel.estado == "COMPLETADA",
                EjecucionMesadaModel.id_transaccion_salida.isnot(None),
                EjecucionMesadaModel.id_transaccion_entrada.isnot(None),
            )
            .first()
        )

        print(
            "DEBUG ejecucion_periodo:",
            {
                "id_mesada": id_mesada,
                "periodo": periodo,
                "resultado": (
                    ejecucion.id_ejecucion
                    if ejecucion
                    else None
                ),
            },
        )

        return ejecucion

    def obtener_tipo_transaccion(self, nombre: str):
        return (
            self.db.query(TipoTransaccionModel)
            .filter(
                TipoTransaccionModel.nombre_tipo_transaccion
                == nombre
            )
            .first()
        )

    def obtener_categoria(
        self,
        nombre: str,
        tipo_categoria: str,
    ):
        return (
            self.db.query(CategoriaModel)
            .filter(
                CategoriaModel.nombre_categoria == nombre,
                CategoriaModel.tipo_categoria == tipo_categoria,
            )
            .first()
        )

    def ejecutar(
        self,
        mesada,
        cuenta_padre,
        cuenta_hijo,
        periodo: str,
        proxima: date,
        id_tipo_salida: int,
        id_tipo_entrada: int,
        id_categoria_salida: int,
        id_categoria_entrada: int,
    ):
        monto = mesada.monto

        # Actualizar saldos
        cuenta_padre.saldo -= monto
        cuenta_hijo.saldo += monto

        # Movimiento de salida del padre
        salida = TransaccionModel(
            monto=monto,
            fecha=datetime.utcnow(),
            descripcion="Mesada parental enviada",
            estado="COMPLETADA",
            id_tipo_transaccion=id_tipo_salida,
            id_cuenta=cuenta_padre.id_cuenta,
            id_categoria=id_categoria_salida,
        )

        # Movimiento de entrada del hijo
        entrada = TransaccionModel(
            monto=monto,
            fecha=datetime.utcnow(),
            descripcion="Mesada parental recibida",
            estado="COMPLETADA",
            id_tipo_transaccion=id_tipo_entrada,
            id_cuenta=cuenta_hijo.id_cuenta,
            id_categoria=id_categoria_entrada,
        )

        self.db.add_all([salida, entrada])
        self.db.flush()

        # Registro de ejecución
        ejecucion = EjecucionMesadaModel(
            id_mesada=mesada.id_mesada,
            periodo=periodo,
            monto=monto,
            id_transaccion_salida=salida.id_transaccion,
            id_transaccion_entrada=entrada.id_transaccion,
            estado="COMPLETADA",
        )

        self.db.add(ejecucion)

        mesada.proxima_ejecucion = proxima

        # Todo se confirma en una sola transacción
        self.db.commit()
        self.db.refresh(ejecucion)

        return ejecucion, proxima

    def rollback(self):
        self.db.rollback()
