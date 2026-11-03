import asyncio
import os
import logging
from aiohttp import web
from aiogram import Bot, Dispatcher
from app.core.config import settings
from app.bot.handlers import start, generator
from app.database.database import init_models
from app.bot.handlers import start, generator, extra

logging.basicConfig(level=logging.INFO)

async def handle_ping(request):
    return web.Response(text="Bot ishlayapti!")

async def start_web_server():
    app = web.Application()
    app.router.add_get('/', handle_ping)
    runner = web.AppRunner(app)
    await runner.steup()
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()

async def main():
    # Jadvallarni bazada yaratish
    await init_models()
    
    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(start.router)
    dp.include_router(generator.router)
    dp.include_router(extra.router)

    logging.info("Starting QR Studio Bot...")
    await start_web_server()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())