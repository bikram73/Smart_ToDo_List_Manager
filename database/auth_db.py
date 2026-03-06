from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

AUTH_DATABASE_URL = os.getenv("AUTH_DATABASE_URL", "sqlite:///./auth.db") # Fallback for local testing

engine = create_engine(AUTH_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_auth_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
