from sqlalchemy import (
    Column,
    Integer,
    Numeric,
    String,
    Date,
    ForeignKey
)

from datetime import date

from app.core.database.base import Base


class CuentaModel(Base):
    __tablename__ = "cuenta"

    id_cuenta = Column(
        Integer,
        primary_key=True,
        index=True
    )

    saldo = Column(
        Numeric(12, 2),
        default=0
    )

    fecha_creacion = Column(
        Date,
        default=date.today
    )

    estado = Column(
        String(20),
        nullable=False
    )

    id_usuario = Column(
        Integer,
        ForeignKey("usuario.id_usuario"),
        unique=True,
        nullable=False
    )