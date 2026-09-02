from sqlalchemy.orm import Session

from app.modules.programacion_ahorro.domain.interface.programacion_repository import ProgramacionAhorroRepository
from app.modules.programacion_ahorro.infrastructure.model.programacion_model import ProgramacionModel


class SqlProgramacionRepository(ProgramacionAhorroRepository):

    def __init__(self, db: Session):
        self.db = db

    def create(self, programacion_data):
        programacion = ProgramacionModel(
            **programacion_data
        )
        self.db.add(programacion)
        self.db.commit()
        self.db.refresh(programacion)
        return programacion