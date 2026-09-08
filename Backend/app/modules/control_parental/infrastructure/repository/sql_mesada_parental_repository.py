from sqlalchemy.orm import Session

from app.modules.control_parental.infrastructure.model.control_parental_model import ControlParentalModel, PermisoParentalModel
from app.modules.control_parental.infrastructure.model.mesada_parental_model import MesadaParentalModel
from app.modules.cuenta.infrastructure.model.cuenta_model import CuentaModel




class SqlMesadaParentalRepository:
    def __init__(self, db: Session):
        self.db = db

    def obtener_vinculo_activo(self, id_padre: int, id_hijo: int):
        return self.db.query(ControlParentalModel).filter(
            ControlParentalModel.id_usuario_parental == id_padre,
            ControlParentalModel.id_usuario_dependiente == id_hijo,
            ControlParentalModel.estado == "ACTIVO",
        ).first()

    def permiso_activo(self, id_control: int, nombre_permiso: str):
        permiso = self.db.query(PermisoParentalModel).filter(
            PermisoParentalModel.id_control == id_control,
            PermisoParentalModel.nombre_permiso == nombre_permiso,
        ).first()
        return bool(permiso and permiso.permitido)

    def obtener_cuentas(self, id_padre: int, id_hijo: int):
        padre = self.db.query(CuentaModel).filter(CuentaModel.id_usuario == id_padre).first()
        hijo = self.db.query(CuentaModel).filter(CuentaModel.id_usuario == id_hijo).first()
        return padre, hijo

    def obtener_activa(self, id_control: int):
        return self.db.query(MesadaParentalModel).filter(
            MesadaParentalModel.id_control == id_control,
            MesadaParentalModel.estado == "ACTIVA",
        ).first()

    def crear(self, model):
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return model

    def guardar(self):
        self.db.commit()

    def rollback(self):
        self.db.rollback()

    @staticmethod
    def model_to_dict(model):
        return {
            "id_mesada": model.id_mesada,
            "id_control": model.id_control,
            "id_cuenta_padre": model.id_cuenta_padre,
            "id_cuenta_hijo": model.id_cuenta_hijo,
            "monto": model.monto,
            "frecuencia": model.frecuencia,
            "fecha_inicio": model.fecha_inicio,
            "fecha_fin": model.fecha_fin,
            "proxima_ejecucion": model.proxima_ejecucion,
            "estado": model.estado,
        }
