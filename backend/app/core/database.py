from sqlalchemy.ext.asyncio import create_async_io_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

# Şimdilik yerel bir SQLite kullanalım ki hemen test edebilesin, 
# sonra PostgreSQL'e kolayca geçeriz.
SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

engine = create_async_io_engine(SQLALCHEMY_DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session