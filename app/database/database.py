from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.database.models.base import Base
from app.database.models.user import User 
from app.database.models.history import History # YANGI QATOR


DATABASE_URL = "sqlite+aiosqlite:///./qr_studio.db"

engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)