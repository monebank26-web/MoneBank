from sqlalchemy import text
from sqlalchemy.orm import Session

from app.modules.programacion_ahorro.domain.interface.programacion_repository import ProgramacionAhorroRepository
from app.modules.ahorro.infrastructure.model.ahorro_model import AhorroModel
from app.modules.programacion_ahorro.infrastructure.model.programacion_model import programacion_model


class SqlAhorroRepository(ProgramacionAhorroRepository):

    def __init__(self, db: Session):
        self.db = db

    def create(self, programacion_data):
        programacion = programacion_model(
            **programacion_data
        )
        self.db.add(programacion)
        self.db.commit()
        self.db.refresh(programacion)
        return programacion

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

    def get_gasto_periodo(self, id_categoria, id_cuenta, fecha_desde, fecha_hasta):
        fila = self.db.execute(
            text(
                "SELECT fn_gasto_categoria_periodo("
                ":id_categoria, :id_cuenta, :fecha_desde, :fecha_hasta) AS total"
            ),
            {"id_categoria": id_categoria, "id_cuenta": id_cuenta,
             "fecha_desde": fecha_desde, "fecha_hasta": fecha_hasta},
        ).first()

        return fila.total if fila else 0

    def get_by_cuenta(self, id_cuenta):
        return (
            self.db.query(AhorroModel)
            .filter(AhorroModel.id_cuenta == id_cuenta)
            .all()
        )

    def descontar_saldo(self, id_cuenta, monto):
        cuenta = (
            self.db.query(CuentaModel)
            .filter(CuentaModel.id_cuenta == id_cuenta)
            .first()
        )

        if not cuenta:
            return None

        cuenta.saldo -= monto
        self.db.commit()
        self.db.refresh(cuenta)
        return cuenta
