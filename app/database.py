from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings

DATABASE_URL = settings.DATABASE_URL



engine = create_engine(DATABASE_URL)
# so this is like a factory that makes sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# this is like mongoose schema
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()