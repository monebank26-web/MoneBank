from sqlalchemy import Column, Date, Integer, Numeric, String

from app.core.database.base import Base


class ProgramacionDetalleModel(Base):
    __tablename__ = "vw_programacion_ahorro_detalle"

    id_programacion_ahorro = Column(Integer, primary_key=True)
    id_ahorro = Column(Integer, nullable=False)
    id_cuenta = Column(Integer, nullable=False)
    nombre_ahorro = Column(String(100), nullable=False)
    monto_periodico = Column(Numeric(12, 2), nullable=False)
    frecuencia = Column(String(20), nullable=False)
    fecha_inicio_vigencia = Column(Date, nullable=False)
    fecha_fin_vigencia = Column(Date, nullable=False)
    proxima_fecha_cobro = Column(Date, nullable=False)
    dias_para_proximo_cobro = Column(Integer, nullable=False)
    estado_programacion = Column(String(20), nullable=False)