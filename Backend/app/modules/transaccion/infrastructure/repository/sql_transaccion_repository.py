from sqlalchemy import text
from sqlalchemy.orm import Session

from app.modules.ahorro.infrastructure.model.ahorro_model import AhorroModel
from app.modules.cuenta.infrastructure.model.cuenta_model import CuentaModel
from app.modules.transaccion.domain.interface.trans_repository import (
    TransaccionRepository
)
from app.modules.transaccion.infrastructure.model.categoria_model import (
    CategoriaModel
)
from app.modules.transaccion.infrastructure.model.tipo_transaccion_model import (
    TipoTransaccionModel
)
from app.modules.transaccion.infrastructure.model.transaccion_model import (
    TransaccionModel
)

ORDEN_PERMITIDO = {"fecha": "v.fecha", "monto": "v.monto"}


class SqlTransaccionesRepository(TransaccionRepository):

    def __init__(self, db: Session):
        self.db = db

    def find_historial(self, usuario_id, filtros):
        condiciones = ["v.id_usuario = :usuario_id"]
        parametros = {"usuario_id": usuario_id}

        if filtros["fecha_inicio"]:
            condiciones.append("v.fecha >= :fecha_inicio")
            parametros["fecha_inicio"] = filtros["fecha_inicio"]

        if filtros["fecha_fin"]:
            condiciones.append("v.fecha <= :fecha_fin")
            parametros["fecha_fin"] = filtros["fecha_fin"]

        if filtros["monto_min"] is not None:
            condiciones.append("v.monto >= :monto_min")
            parametros["monto_min"] = filtros["monto_min"]

        if filtros["monto_max"] is not None:
            condiciones.append("v.monto <= :monto_max")
            parametros["monto_max"] = filtros["monto_max"]

        if filtros["busqueda"]:
            condiciones.append("v.descripcion ILIKE :busqueda")
            parametros["busqueda"] = f"%{filtros['busqueda']}%"

        if filtros["id_tipo_transaccion"]:
            condiciones.append("v.id_tipo_transaccion = :id_tipo_transaccion")
            parametros["id_tipo_transaccion"] = filtros["id_tipo_transaccion"]

        if filtros["id_categoria"]:
            condiciones.append("v.id_categoria = :id_categoria")
            parametros["id_categoria"] = filtros["id_categoria"]

        where = " AND ".join(condiciones)
        columna = ORDEN_PERMITIDO[filtros["ordenar_por"]]
        direccion = "ASC" if filtros["orden"] == "asc" else "DESC"

        total = self.db.execute(
            text(f"SELECT COUNT(*) FROM vw_historial_transacciones v WHERE {where}"),
            parametros
        ).scalar()

        filas = self.db.execute(
            text(
                f"SELECT * FROM vw_historial_transacciones v WHERE {where} "
                f"ORDER BY {columna} {direccion}, v.id_transaccion {direccion} "
                "LIMIT :limite OFFSET :offset"
            ),
            {
                **parametros,
                "limite": filtros["por_pagina"],
                "offset": (filtros["pagina"] - 1) * filtros["por_pagina"]
            }
        )

        return [dict(fila._mapping) for fila in filas], total

    def find_categorias(self):
        resultado = (
            self.db.query(CategoriaModel.id_categoria, CategoriaModel.nombre_categoria)
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
