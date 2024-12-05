from .models import Base
from app.core import settings

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

# Create engine, define maximum concurrent connections
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False
)

# Create session
SessionLocal = sessionmaker(
    autocommit=False,   
    autoflush=False, 
    bind=engine, 
    class_=AsyncSession
)

# Async function to get db
async def get_db():
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

# Create tables if they don't already exist
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)