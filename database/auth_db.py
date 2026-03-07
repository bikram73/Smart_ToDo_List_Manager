from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

AUTH_DATABASE_URL = os.getenv("AUTH_DATABASE_URL", "sqlite:///./auth.db") # Fallback for local testing

# Vercel/Neon uses a "postgres://" URL, but SQLAlchemy requires "postgresql://"
if AUTH_DATABASE_URL and AUTH_DATABASE_URL.startswith("postgres://"):
    AUTH_DATABASE_URL = AUTH_DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(AUTH_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_auth_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
