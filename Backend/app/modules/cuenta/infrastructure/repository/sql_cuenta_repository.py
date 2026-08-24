from sqlalchemy.orm import Session

from app.modules.cuenta.domain.interface.cuenta_repository import CuentaRepository
from app.modules.cuenta.infrastructure.model.cuenta_model import CuentaModel


class SqlCuentaRepository(CuentaRepository):

    def __init__(self, db: Session):
        self.db = db

    def create(self, cuenta_data):
        cuenta = CuentaModel(**cuenta_data)
        self.db.add(cuenta)
        self.db.commit()
        self.db.refresh(cuenta)
        return cuenta

    def get_all(self):
        return self.db.query(CuentaModel).all()

    def get_by_id(self, id_cuenta):
        return (
            self.db.query(CuentaModel)
            .filter(CuentaModel.id_cuenta == id_cuenta)
            .first()
        )

    def delete(self, id_cuenta):
        cuenta = self.get_by_id(id_cuenta)

        if not cuenta:
            return None

        self.db.delete(cuenta)
        self.db.commit()

        return {"mensaje": "Cuenta eliminada"}
