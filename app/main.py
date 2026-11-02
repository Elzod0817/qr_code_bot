import asyncio
import logging
from aiogram import Bot, Dispatcher
from app.core.config import settings
from app.bot.handlers import start, generator
from app.database.database import init_models
from app.bot.handlers import start, generator, extra

logging.basicConfig(level=logging.INFO)

async def main():
    # Jadvallarni bazada yaratish
    await init_models()
    
    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(start.router)
    dp.include_router(generator.router)
    dp.include_router(extra.router)

    logging.info("Starting QR Studio Bot...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())