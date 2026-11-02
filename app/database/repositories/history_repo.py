from sqlalchemy import select, func
from app.database.database import AsyncSessionLocal
from app.database.models.history import History

async def add_qr_history(telegram_id: int, qr_data: str):
    """Yaratilgan QR kod ma'lumotini bazaga yozish"""
    async with AsyncSessionLocal() as session:
        record = History(telegram_id=telegram_id, qr_data=qr_data)
        session.add(record)
        await session.commit()
        from sqlalchemy import select, func

async def get_history_count():
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(func.count(History.id)))
        return result.scalar()

async def get_user_history(telegram_id: int, limit: int = 5):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(History).where(History.telegram_id == telegram_id).order_by(History.created_at.desc()).limit(limit)
        )
        return result.scalars().all()