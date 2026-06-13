from sqlalchemy.orm import sessionmaker
from app.core.database.connection import engine

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)