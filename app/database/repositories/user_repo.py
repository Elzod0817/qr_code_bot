from sqlalchemy import select, func
from app.database.database import AsyncSessionLocal
from app.database.models.user import User

async def get_or_create_user(telegram_id: int, username: str, full_name: str, language: str = "uz"):
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.telegram_id == telegram_id))
        user = result.scalar_one_or_none()
        
        if not user:
            user = User(
                telegram_id=telegram_id, 
                username=username, 
                full_name=full_name, 
                language=language
            )
            session.add(user)
            await session.commit()
            await session.refresh(user)
            
        return user
    from sqlalchemy import func

async def get_users_count():
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(func.count(User.id)))
        return result.scalar()