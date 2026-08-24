from sqlalchemy.orm import Session

from app.modules.ahorro.domain.interface.ahorro_repository import AhorroRepository
from app.modules.ahorro.infrastructure.model.ahorro_model import AhorroModel


class SqlAhorroRepository(AhorroRepository):

    def __init__(self, db: Session):
        self.db = db

    def create(self, ahorro_data):
        ahorro = AhorroModel(
            **ahorro_data,
            saldo_actual=ahorro_data["saldo_inicial"]
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
