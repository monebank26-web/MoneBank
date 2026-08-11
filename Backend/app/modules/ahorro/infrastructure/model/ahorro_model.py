from sqlalchemy import (
    Column,
    Integer,
    String,
    Numeric,
    Boolean,
    Date
)

from datetime import date

from app.core.database.base import Base


class AhorroModel(Base):
    __tablename__ = "ahorro"

    id_ahorro = Column(Integer, primary_key=True, index=True)

    nombre = Column(String(100), nullable=False)

    monto_objetivo = Column(Numeric(12, 2))
    saldo_inicial = Column(Numeric(12, 2))
    saldo_actual = Column(Numeric(12, 2))

    ahorro_automatico = Column(Boolean)

    fecha_creacion = Column(
        Date,
        default=date.today
    )

    estado = Column(String(20))

    id_tipo_ahorro = Column(Integer)
    id_categoria = Column(Integer)
    id_cuenta = Column(Integer)