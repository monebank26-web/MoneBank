from app.modules.ahorro.infrastucture.model.ahorro_model import AhorroModel


class SqlAhorroRepository:

    def create(self, db, ahorro_data):

        ahorro = AhorroModel(
            **ahorro_data,
            saldo_actual=ahorro_data["saldo_inicial"]
        )

        db.add(ahorro)
        db.commit()
        db.refresh(ahorro)

        return ahorro

    def get_all(self, db):
        return db.query(AhorroModel).all()

    def get_by_id(self, db, id_ahorro):

        return (
            db.query(AhorroModel)
            .filter(
                AhorroModel.id_ahorro == id_ahorro
            )
            .first()
        )

    def update(
        self,
        db,
        id_ahorro,
        ahorro_data
    ):

        ahorro = (
            db.query(AhorroModel)
            .filter(
                AhorroModel.id_ahorro == id_ahorro
            )
            .first()
        )

        if not ahorro:
            return None

        for key, value in ahorro_data.items():
            setattr(ahorro, key, value)

        db.commit()
        db.refresh(ahorro)

        return ahorro

    def delete(
        self,
        db,
        id_ahorro
    ):

        ahorro = (
            db.query(AhorroModel)
            .filter(
                AhorroModel.id_ahorro == id_ahorro
            )
            .first()
        )

        if not ahorro:
            return None

        db.delete(ahorro)
        db.commit()

        return {
            "mensaje": "Ahorro eliminado"
        }