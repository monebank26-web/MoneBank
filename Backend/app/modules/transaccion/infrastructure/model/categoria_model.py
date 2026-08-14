from sqlalchemy import (
    Column,
    Integer,
    String
)

from app.core.database.base import Base


class CategoriaModel(Base):

    __tablename__ = "categoria"

    id_categoria = Column(
        Integer,
        primary_key=True,
        index=True
    )

    nombre = Column(
        String(100),
        nullable=False
    )

    descripcion = Column(
        String(255),
        nullable=True
    )
