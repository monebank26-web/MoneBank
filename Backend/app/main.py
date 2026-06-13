from fastapi import FastAPI
from app.core.database.connection import engine
from app.core.database.base import Base

app = FastAPI()

Base.metadata.create_all(bind=engine)