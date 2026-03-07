from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

TODO_DATABASE_URL = os.getenv("TODO_DATABASE_URL", "sqlite:///./todo.db") # Fallback for local testing

# Vercel/Neon uses a "postgres://" URL, but SQLAlchemy requires "postgresql://"
if TODO_DATABASE_URL and TODO_DATABASE_URL.startswith("postgres://"):
    TODO_DATABASE_URL = TODO_DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(TODO_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_todo_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
