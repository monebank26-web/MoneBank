from sqlalchemy import Column, DateTime, Integer, Numeric, String

from app.core.database.base import Base


class HistorialTransaccionModel(Base):
    __tablename__ = "vw_historial_transacciones"

    id_usuario = Column(Integer, nullable=False)
    nombres = Column(String(100), nullable=False)
    apellidos = Column(String(100), nullable=False)
    id_cuenta = Column(Integer, nullable=False)
    id_transaccion = Column(Integer, primary_key=True)
    id_tipo_transaccion = Column(Integer, nullable=False)
    tipo_transaccion = Column(String(50), nullable=False)
    monto = Column(Numeric(12, 2), nullable=False)
    fecha = Column(DateTime, nullable=False)
    descripcion = Column(String(255), nullable=True)
    estado_transaccion = Column(String(20), nullable=False)
    id_categoria = Column(Integer, nullable=False)
    nombre_categoria = Column(String(60), nullable=False)
    id_ahorro = Column(Integer, nullable=True)
    nombre_ahorro = Column(String(100), nullable=True)
    nombre_tipo_ahorro = Column(String(100), nullable=True)
