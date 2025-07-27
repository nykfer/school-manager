from sqlmodel import Session, SQLModel, create_engine
from dotenv import load_dotenv
import os

load_dotenv()

engine_db = create_engine(os.getenv("POSTGRES_URL"), echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine_db)

def get_session_db():
    with Session(engine_db) as session:
        yield session
