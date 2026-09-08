from sqlalchemy import (
    Column,
    Integer,
    String,
    Numeric,
    Date
)

from app.core.database.base import Base


class ProgramacionModel(Base):
    __tablename__ = "programacion_ahorro"


    id_programacion_ahorro = Column(Integer, primary_key=True, index=True)
    monto_periodico = Column(Numeric(12, 2))
    fecha_cobro = Column(Date)
    frecuencia = Column(String(20))
    fecha_inicio = Column(Date)
    fecha_fin = Column(Date)
    estado = Column(String(20))