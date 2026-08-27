from sqlalchemy import (
    Column,
    Integer,
    String
)

from app.core.database.base import Base


class TipoTransaccionModel(Base):

    __tablename__ = "tipo_transaccion"

    id_tipo_transaccion = Column(
        Integer,
        primary_key=True,
        index=True
    )

    nombre_tipo_transaccion = Column(
        String(50),
        nullable=False,
        unique=True
    )
