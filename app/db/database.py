from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from app.core.config import settings

# Convert sync URL to async URL if necessary (e.g., postgresql:// to postgresql+asyncpg://)
# We are using psycopg2 so we'll use sync engine or asyncpg. Actually, psycopg2 is synchronous.
# Wait, let's use standard sync SQLAlchemy engine to avoid async pg complexities since standard psycopg2 is requested in requirements.
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
