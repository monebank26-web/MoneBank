from sqlalchemy import Column, Integer, String, Date
from datetime import date

from app.core.database.base import Base


class UsuarioModel(Base):
    __tablename__ = "usuario"

    id_usuario = Column(Integer, primary_key=True, index=True)

    nombres = Column(String(80), nullable=False)
    apellidos = Column(String(100), nullable=False)

    correo = Column(String(150), unique=True, nullable=False)

    contrasena = Column(String(100), nullable=False)

    fecha_creacion = Column(Date, default=date.today)

    estado = Column(String(20), nullable=False)

    id_rol = Column(Integer)
    id_tipo_usuario = Column(Integer)