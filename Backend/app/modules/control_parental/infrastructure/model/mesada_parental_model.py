from datetime import datetime

from sqlalchemy import (
    Column,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
)

from app.core.database.base import Base


class MesadaParentalModel(Base):
    __tablename__ = "mesada_parental"

    id_mesada = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    id_control = Column(
        Integer,
        ForeignKey(
            "control_parental.id_control"
        ),
        nullable=False,
    )

    id_cuenta_padre = Column(
        Integer,
        ForeignKey(
            "cuenta.id_cuenta"
        ),
        nullable=False,
    )

    id_cuenta_hijo = Column(
        Integer,
        ForeignKey(
            "cuenta.id_cuenta"
        ),
        nullable=False,
    )

    monto = Column(
        Numeric(12, 2),
        nullable=False,
    )

    frecuencia = Column(
        String(20),
        nullable=False,
    )

    fecha_inicio = Column(
        Date,
        nullable=False,
    )

    fecha_fin = Column(
        Date,
        nullable=True,
    )

    proxima_ejecucion = Column(
        Date,
        nullable=True,
    )

    estado = Column(
        String(20),
        nullable=False,
        default="ACTIVA",
    )

    fecha_creacion = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
    )

    fecha_actualizacion = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
