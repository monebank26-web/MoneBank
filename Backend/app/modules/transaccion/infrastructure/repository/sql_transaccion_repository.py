from sqlalchemy.orm import Session

from app.modules.ahorro.infrastructure.model.ahorro_model import AhorroModel
from app.modules.ahorro.infrastructure.model.tipo_ahorro_model import (
    TipoAhorroModel
)
from app.modules.cuenta.infrastructure.model.cuenta_model import CuentaModel
from app.modules.transaccion.domain.interface.trans_repository import (
    TransaccionRepository
)
from app.modules.transaccion.infrastructure.model.categoria_model import (
    CategoriaModel
)
from app.modules.transaccion.infrastructure.model.historial_transaccion_model import (
    HistorialTransaccionModel
)
from app.modules.transaccion.infrastructure.model.transaccion_model import (
    TransaccionModel
)

from app.modules.transaccion.infrastructure.model.tipo_transaccion_model import (
    TipoTransaccionModel
)

ORDEN_PERMITIDO = {
    "fecha": HistorialTransaccionModel.fecha,
    "monto": HistorialTransaccionModel.monto,
}


class SqlTransaccionesRepository(TransaccionRepository):

    def __init__(self, db: Session):
        self.db = db

    def find_historial(self, usuario_id, filtros):
        consulta = self.db.query(HistorialTransaccionModel).filter(
            HistorialTransaccionModel.id_usuario == usuario_id
        )

        if filtros["fecha_inicio"]:
            consulta = consulta.filter(
                HistorialTransaccionModel.fecha >= filtros["fecha_inicio"]
            )

        if filtros["fecha_fin"]:
            consulta = consulta.filter(
                HistorialTransaccionModel.fecha <= filtros["fecha_fin"]
            )

        if filtros["monto_min"] is not None:
            consulta = consulta.filter(
                HistorialTransaccionModel.monto >= filtros["monto_min"]
            )

        if filtros["monto_max"] is not None:
            consulta = consulta.filter(
                HistorialTransaccionModel.monto <= filtros["monto_max"]
            )

        if filtros["busqueda"]:
            consulta = consulta.filter(
                HistorialTransaccionModel.descripcion.ilike(
                    f"%{filtros['busqueda']}%"
                )
            )

        if filtros["id_tipo_transaccion"]:
            consulta = consulta.filter(
                HistorialTransaccionModel.id_tipo_transaccion
                == filtros["id_tipo_transaccion"]
            )

        if filtros["id_categoria"]:
            consulta = consulta.filter(
                HistorialTransaccionModel.id_categoria == filtros["id_categoria"]
            )

        columna = ORDEN_PERMITIDO[filtros["ordenar_por"]]
        if filtros["orden"] == "asc":
            consulta = consulta.order_by(
                columna.asc(), HistorialTransaccionModel.id_transaccion.asc()
            )
        else:
            consulta = consulta.order_by(
                columna.desc(), HistorialTransaccionModel.id_transaccion.desc()
            )

        total = consulta.count()
        filas = (
            consulta.offset((filtros["pagina"] - 1) * filtros["por_pagina"])
            .limit(filtros["por_pagina"])
            .all()
        )

        return filas, total

    def find_detalle(self, id_usuario, id_transaccion):
        return (
            self.db.query(HistorialTransaccionModel)
            .filter(
                HistorialTransaccionModel.id_usuario == id_usuario,
                HistorialTransaccionModel.id_transaccion == id_transaccion,
            )
            .first()
        )

    def find_categorias(self):
        resultado = (
            self.db.query(
                CategoriaModel.id_categoria,
                CategoriaModel.nombre_categoria,
                CategoriaModel.tipo_categoria,
            )
            .order_by(CategoriaModel.nombre_categoria)
            .all()
        )
        return [dict(fila._mapping) for fila in resultado]

    def create(self, transaccion_data):
        transaccion = TransaccionModel(**transaccion_data)
        self.db.add(transaccion)
        self.db.commit()
        self.db.refresh(transaccion)
        return transaccion

    def get_cuenta(self, id_cuenta):
        return (
            self.db.query(CuentaModel)
            .filter(CuentaModel.id_cuenta == id_cuenta)
            .first()
        )

    def existe_categoria(self, id_categoria):
        return (
            self.db.query(CategoriaModel)
            .filter(CategoriaModel.id_categoria == id_categoria)
            .first()
            is not None
        )

    def get_tipo_transaccion(self, nombre):
        return (
            self.db.query(TipoTransaccionModel)
            .filter(TipoTransaccionModel.nombre_tipo_transaccion == nombre)
            .first()
        )

    def get_ahorro(self, id_ahorro):
        return (
            self.db.query(AhorroModel)
            .filter(AhorroModel.id_ahorro == id_ahorro)
            .first()
        )

    def descontar_saldo(self, id_cuenta, monto):
        cuenta = self.get_cuenta(id_cuenta)

        if not cuenta:
            return None

        cuenta.saldo -= monto
        self.db.commit()
        self.db.refresh(cuenta)
        return cuenta
        
    def aumentar_saldo(self, id_cuenta, monto):
            cuenta = self.get_cuenta(id_cuenta)
    
            if not cuenta:
                return None
    
            cuenta.saldo += monto
            self.db.commit()
            self.db.refresh(cuenta)
            return cuenta

    
    def get_tipo_ahorro(self, nombre):
        return (
            self.db.query(TipoAhorroModel)
            .filter(TipoAhorroModel.nombre_tipo_ahorro == nombre)
            .first()
        )

    def sumar_saldo_ahorro(self, id_ahorro, monto):
        ahorro = (
            self.db.query(AhorroModel)
            .filter(AhorroModel.id_ahorro == id_ahorro)
            .first()
        )

        if not ahorro:
            return None

        ahorro.saldo_actual += monto
        self.db.commit()
        self.db.refresh(ahorro)
        return ahorro
