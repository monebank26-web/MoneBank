from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    Numeric
)

from datetime import date

from app.core.database.base import Base


class TransaccionModel(Base):

    __tablename__ = "transaccion"

    id_transaccion = Column(
        Integer,
        primary_key=True,
        index=True
    )

    monto = Column(
        Numeric(12, 2),
        nullable=False
    )

    fecha = Column(
        Date,
        default=date.today
    )

    referencia = Column(
        String(150),
        nullable=True
    )

    descripcion = Column(
        String(255),
        nullable=True
    )

    tipo = Column(
        String(20),
        nullable=False
    )

    id_tipo_transaccion = Column(Integer)

    id_cuenta = Column(Integer)

    id_categoria = Column(Integer)

    id_ahorro = Column(Integer)