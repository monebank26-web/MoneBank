from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
)

from app.core.database.base import Base


class EjecucionMesadaModel(Base):
    __tablename__ = "mesada_parental_ejecucion"

    id_ejecucion = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    id_mesada = Column(
        Integer,
        ForeignKey("mesada_parental.id_mesada"),
        nullable=False,
    )

    periodo = Column(
        String(20),
        nullable=False,
    )

    monto = Column(
        Numeric(12, 2),
        nullable=False,
    )

    fecha_ejecucion = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
    )

    id_transaccion_salida = Column(
        Integer,
        nullable=True,
    )

    id_transaccion_entrada = Column(
        Integer,
        nullable=True,
    )

    estado = Column(
        String(20),
        nullable=False,
        default="COMPLETADA",
    )
