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

    def update_estado(self, programacion_id, nuevo_estado):
            programacion = (
                self.db.query(ProgramacionModel)
                .filter(ProgramacionModel.id_programacion == programacion_id)
                .first()
            )
    
            if not programacion:
                return None
    
            programacion.Estado = nuevo_estado
    
            self.db.commit()
            self.db.refresh(programacion)
            return programacion
