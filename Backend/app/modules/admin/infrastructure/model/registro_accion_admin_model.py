from sqlalchemy import Column, DateTime, Integer, String, Text, func

from app.core.database.base import Base


class RegistroAccionAdminModel(Base):

    __tablename__ = "registro_accion_admin"

    id_registro_accion = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    id_admin = Column(
        Integer,
        nullable=False,
    )

    accion = Column(
        String(60),
        nullable=False,
    )

    id_usuario_afectado = Column(
        Integer,
        nullable=True,
    )

    detalle = Column(
        Text,
        nullable=True,
    )

    fecha = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
