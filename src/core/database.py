from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from src.core.settings import settings

engine = create_async_engine(settings.POSTGRES_URL)

SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

Base = declarative_base()


async def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        await db.close()
