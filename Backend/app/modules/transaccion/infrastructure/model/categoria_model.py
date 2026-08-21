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

    nombre_categoria = Column(
        String(60),
        nullable=False
    )

    tipo_categoria = Column(
        String(50),
        nullable=False
    )

    descripcion = Column(
        String(255),
        nullable=True
    )

    estado = Column(
        String(20),
        nullable=False
    )
