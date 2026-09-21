from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Numeric
)

from app.core.database.base import Base
from app.core.utils.fechas import ahora_colombia


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
        DateTime,
        default=ahora_colombia
    )

    descripcion = Column(
        String(255),
        nullable=True
    )

    estado = Column(
        String(20),
        nullable=False,
        default="COMPLETADA"
    )

    id_tipo_transaccion = Column(Integer)

    id_cuenta = Column(Integer)

    id_categoria = Column(Integer)

    id_ahorro = Column(Integer)
