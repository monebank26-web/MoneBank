from app.modules.cuenta.infrastucture.model.cuenta_model import CuentaModel


class SqlCuentaRepository:

    def create(self, db, cuenta_data):

        cuenta = CuentaModel(**cuenta_data)

        db.add(cuenta)
        db.commit()
        db.refresh(cuenta)

        return cuenta

    def get_all(self, db):
        return db.query(CuentaModel).all()

    def get_by_id(self, db, id_cuenta):

        return (
            db.query(CuentaModel)
            .filter(
                CuentaModel.id_cuenta == id_cuenta
            )
            .first()
        )

    def delete(self, db, id_cuenta):

        cuenta = self.get_by_id(
            db,
            id_cuenta
        )

        if not cuenta:
            return None

        db.delete(cuenta)
        db.commit()

        return {
            "mensaje": "Cuenta eliminada"
        }