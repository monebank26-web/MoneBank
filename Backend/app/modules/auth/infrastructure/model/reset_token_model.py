from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey

from app.core.database.base import Base


class ResetTokenModel(Base):
    __tablename__ = "password_reset_token"

    id = Column(Integer, primary_key=True, index=True)

    usuario_id = Column(
        Integer,
        ForeignKey("usuario.id_usuario", ondelete="CASCADE"),
        nullable=False
    )

    token_hash = Column(String(64), nullable=False, unique=True, index=True)

    fecha_creacion = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    fecha_expiracion = Column(DateTime(timezone=True), nullable=False)

    usado = Column(Boolean, default=False)
