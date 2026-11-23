from sqlalchemy.orm import Session

from app.modules.programacion_ahorro.domain.entity.programacion_ahorro import ProgramacionAhorro
from app.modules.programacion_ahorro.domain.interface.programacion_repository import ProgramacionAhorroRepository
from app.modules.programacion_ahorro.infrastructure.model.programacion_model import ProgramacionModel
from app.modules.programacion_ahorro.infrastructure.model.programacion_detalle_model import ProgramacionDetalleModel


class SqlProgramacionRepository(ProgramacionAhorroRepository):

    def __init__(self, db: Session):
        self.db = db

    def create(self, programacion_data):
        programacion = ProgramacionModel(
            **programacion_data
        )
        self.db.add(programacion)
        self.db.flush()
        self.db.refresh(programacion)
        return programacion

    def get_by_id(self, programacion_id):
        return (
            self.db.query(ProgramacionModel)
            .filter(
                ProgramacionModel.id_programacion_ahorro == programacion_id
            )
            .first()
        )

    def get_para_procesar(self, programacion_id):
        return (
            self.db.query(ProgramacionModel)
            .filter(
                ProgramacionModel.id_programacion_ahorro == programacion_id
            )
            .with_for_update(skip_locked=True)
            .first()
        )

    def obtener_vencidas(self, hoy):
        return (
            self.db.query(ProgramacionModel)
            .filter(ProgramacionModel.estado == ProgramacionAhorro.ESTADO_ACTIVA)
            .filter(ProgramacionModel.fecha_cobro <= hoy)
            .order_by(
                ProgramacionModel.fecha_cobro.asc(),
                ProgramacionModel.id_programacion_ahorro.asc(),
            )
            .all()
        )

    def actualizar_fecha_cobro(
        self,
        programacion_id,
        nueva_fecha,
        nuevo_estado=None,
    ):
        programacion = self.get_by_id(programacion_id)

        if not programacion:
            return None

        programacion.fecha_cobro = nueva_fecha

        if nuevo_estado is not None:
            programacion.estado = nuevo_estado

        self.db.flush()
        self.db.refresh(programacion)
        return programacion

    def obtener_por_ahorro(self, id_ahorro):
        return (
            self.db.query(ProgramacionModel)
            .filter(ProgramacionModel.id_ahorro == id_ahorro)
            .first()
        )

    def update_estado(self, programacion_id, nuevo_estado):
        programacion = self.get_by_id(programacion_id)

        if not programacion:
            return None

        programacion.estado = nuevo_estado

        self.db.flush()
        self.db.refresh(programacion)
        return programacion

    def update_periodicidad(self, programacion_id, monto_periodico, frecuencia):
        programacion = self.get_by_id(programacion_id)

        if not programacion:
            return None

        programacion.monto_periodico = monto_periodico
        programacion.frecuencia = frecuencia

        self.db.flush()
        self.db.refresh(programacion)
        return programacion

    def obtener_detalles_por_cuenta(self, id_cuenta):
        return (
            self.db.query(ProgramacionDetalleModel)
            .filter(ProgramacionDetalleModel.id_cuenta == id_cuenta)
            .order_by(ProgramacionDetalleModel.proxima_fecha_cobro.asc())
            .all()
        )
