from sqlalchemy import text
from sqlalchemy.orm import Session

from app.modules.ahorro.domain.interface.ahorro_repository import AhorroRepository
from app.modules.ahorro.infrastructure.model.ahorro_model import AhorroModel
from app.modules.ahorro.infrastructure.model.tipo_ahorro_model import TipoAhorroModel
from app.modules.cuenta.infrastructure.model.cuenta_model import CuentaModel
from app.modules.transaccion.infrastructure.model.categoria_model import CategoriaModel


class SqlAhorroRepository(AhorroRepository):

    def __init__(self, db: Session):
        self.db = db

    def create(self, ahorro_data):
        ahorro = AhorroModel(
            **ahorro_data,
            saldo_actual=ahorro_data.get("saldo_inicial") or 0
        )
        self.db.add(ahorro)
        self.db.commit()
        self.db.refresh(ahorro)
        return ahorro

    def get_all(self):
        return self.db.query(AhorroModel).all()

    def get_by_id(self, id_ahorro):
        return (
            self.db.query(AhorroModel)
            .filter(AhorroModel.id_ahorro == id_ahorro)
            .first()
        )

    def update(self, id_ahorro, ahorro_data):
        ahorro = (
            self.db.query(AhorroModel)
            .filter(AhorroModel.id_ahorro == id_ahorro)
            .first()
        )

        if not ahorro:
            return None

        for key, value in ahorro_data.items():
            setattr(ahorro, key, value)

        self.db.commit()
        self.db.refresh(ahorro)
        return ahorro

    def delete(self, id_ahorro):
        ahorro = (
            self.db.query(AhorroModel)
            .filter(AhorroModel.id_ahorro == id_ahorro)
            .first()
        )

        if not ahorro:
            return None

        self.db.delete(ahorro)
        self.db.commit()

        return {"mensaje": "Ahorro eliminado"}

    def get_cuenta_por_usuario(self, id_usuario):
        return (
            self.db.query(CuentaModel)
            .filter(CuentaModel.id_usuario == id_usuario)
            .first()
        )

    def get_tipo_ahorro(self, nombre):
        return (
            self.db.query(TipoAhorroModel)
            .filter(TipoAhorroModel.nombre_tipo_ahorro == nombre)
            .first()
        )

    def get_categoria(self, id_categoria):
        return (
            self.db.query(CategoriaModel)
            .filter(CategoriaModel.id_categoria == id_categoria)
            .first()
        )

    def get_by_cuenta_y_tipo(self, id_cuenta, nombre_tipo_ahorro):
        return (
            self.db.query(AhorroModel)
            .join(
                TipoAhorroModel,
                TipoAhorroModel.id_tipo_ahorro == AhorroModel.id_tipo_ahorro
            )
            .filter(
                AhorroModel.id_cuenta == id_cuenta,
                TipoAhorroModel.nombre_tipo_ahorro == nombre_tipo_ahorro
            )
            .all()
        )

    def get_metas_activas(self, id_cuenta):
        resultado = self.db.execute(
            text("SELECT * FROM vw_metas_activas WHERE id_cuenta = :id_cuenta"),
            {"id_cuenta": id_cuenta},
        )
        return [dict(row._mapping) for row in resultado]

    def get_progreso(self, id_ahorro):
        fila = self.db.execute(
            text(
                "SELECT fn_porcentaje_meta(:id_ahorro) AS porcentaje_avance, "
                "fn_dinero_faltante(:id_ahorro) AS monto_faltante"
            ),
            {"id_ahorro": id_ahorro},
        ).first()

        if not fila:
            return None

        return {
            "porcentaje_avance": fila.porcentaje_avance,
            "monto_faltante": fila.monto_faltante,
        }
