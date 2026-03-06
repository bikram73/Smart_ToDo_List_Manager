from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

TODO_DATABASE_URL = os.getenv("TODO_DATABASE_URL", "sqlite:///./todo.db") # Fallback for local testing

engine = create_engine(TODO_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_todo_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
