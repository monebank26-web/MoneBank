from datetime import datetime, timezone
from sqlalchemy import Boolean, Column, DateTime, Integer, String, ForeignKey
from app.core.database.base import Base

class SolicitudControlParentalModel(Base):
    __tablename__ = "control_parental_solicitud"
    id_solicitud = Column(Integer, primary_key=True, index=True)
    id_usuario_solicitante = Column(Integer, ForeignKey("usuario.id_usuario", ondelete="CASCADE"), nullable=False)
    id_usuario_destino = Column(Integer, ForeignKey("usuario.id_usuario", ondelete="CASCADE"), nullable=False)
    id_control = Column(Integer, ForeignKey("control_parental.id_control", ondelete="CASCADE"), nullable=True)
    tipo_operacion = Column(String(20), nullable=False)
    correo_confirmacion = Column(String(150), nullable=False)
    nombre_confirmacion = Column(String(100), nullable=True)
    token_hash = Column(String(64), nullable=False, unique=True, index=True)
    fecha_creacion = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    fecha_expiracion = Column(DateTime(timezone=True), nullable=False)
    intentos_fallidos = Column(Integer, nullable=False, default=0)
    usado = Column(Boolean, nullable=False, default=False)
    estado = Column(String(20), nullable=False, default="PENDIENTE")
