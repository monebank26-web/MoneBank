from datetime import date

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    Date,
    ForeignKey,
    Integer,
    String,
)

from app.core.database.base import Base


class ControlParentalModel(Base):
    __tablename__ = "control_parental"

    id_control = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    permiso_monitoreo = Column(
        Boolean,
        nullable=False,
        default=True,
    )

    fecha_inicio = Column(
        Date,
        nullable=False,
        default=date.today,
    )

    fecha_fin = Column(
        Date,
        nullable=True,
    )

    estado = Column(
        String(20),
        nullable=False,
        default="ACTIVO",
    )

    id_usuario_parental = Column(
        Integer,
        ForeignKey("usuario.id_usuario"),
        nullable=False,
    )

    id_usuario_dependiente = Column(
        Integer,
        ForeignKey("usuario.id_usuario"),
        nullable=False,
    )

    __table_args__ = (
        CheckConstraint(
            "id_usuario_parental <> id_usuario_dependiente",
            name="control_parental_check",
        ),
        CheckConstraint(
            "estado IN ('ACTIVO', 'FINALIZADO')",
            name="control_parental_estado_check",
        ),
    )
class PermisoParentalModel(Base):
    __tablename__ = "control_parental_permiso"

    id_permiso = Column(Integer, primary_key=True)
    id_control = Column(Integer, ForeignKey("control_parental.id_control", ondelete="CASCADE"), nullable=False)
    nombre_permiso = Column(String(60), nullable=False)
    permitido = Column(Boolean, nullable=False, default=False)
    fecha_actualizacion = Column(Date, nullable=False)
