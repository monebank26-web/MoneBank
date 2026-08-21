from sqlalchemy import (
    Column,
    Integer,
    String
)

from app.core.database.base import Base


class TipoAhorroModel(Base):

    __tablename__ = "tipo_ahorro"

    id_tipo_ahorro = Column(
        Integer,
        primary_key=True,
        index=True
    )

    nombre_tipo_ahorro = Column(
        String(30),
        nullable=False,
        unique=True
    )
