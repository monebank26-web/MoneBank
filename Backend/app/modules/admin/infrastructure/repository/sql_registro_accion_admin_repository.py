from sqlalchemy.orm import Session

from app.modules.admin.domain.interface.registro_accion_admin_repository import (
    RegistroAccionAdminRepository,
)
from app.modules.admin.infrastructure.model.registro_accion_admin_model import (
    RegistroAccionAdminModel,
)


class SqlRegistroAccionAdminRepository(RegistroAccionAdminRepository):

    def __init__(self, db: Session):
        self.db = db

    def registrar(
        self,
        id_admin,
        accion,
        id_usuario_afectado=None,
        detalle=None,
    ):
        registro = RegistroAccionAdminModel(
            id_admin=id_admin,
            accion=accion,
            id_usuario_afectado=id_usuario_afectado,
            detalle=detalle,
        )

        self.db.add(registro)
        self.db.commit()
        self.db.refresh(registro)

        return registro

    def listar(self, limite=50):
        return (
            self.db.query(RegistroAccionAdminModel)
            .order_by(
                RegistroAccionAdminModel.fecha.desc(),
                RegistroAccionAdminModel.id_registro_accion.desc(),
            )
            .limit(limite)
            .all()
        )
