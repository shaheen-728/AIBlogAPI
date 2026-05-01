import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
DATABASE_URL = os.getenv("DATABASE_URL")
print("DB URL:", os.getenv("DATABASE_URL"))
engine = create_engine(DATABASE_URL)
session = sessionmaker(bind=engine,autoflush=False,autocommit=False)

class Base(DeclarativeBase):
    pass

def get_db():
    with session() as db:
        yield db

