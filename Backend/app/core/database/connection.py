from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

print("DB_USER:", repr(DB_USER))
print("DB_PASSWORD:", repr(DB_PASSWORD))
print("DB_HOST:", repr(DB_HOST))
print("DB_PORT:", repr(DB_PORT))
print("DB_NAME:", repr(DB_NAME))

DATABASE_URL = (
    f"postgresql://{DB_USER}:"
    f"{DB_PASSWORD}@"
    f"{DB_HOST}:"
    f"{DB_PORT}/"
    f"{DB_NAME}"
)

print("DATABASE_URL:", repr(DATABASE_URL))

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()