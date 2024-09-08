# app/__main__.py
import asyncio
import logging
import uvicorn

from aiogram_dialog import setup_dialogs
from fastapi import FastAPI
from app.core.db_helper import db_helper
from app.tgbot.middlewares.db_session import DbSessionMiddleware

from app.tgbot.bot import dp, bot
from app.tgbot.dialogs.users.users_dialog import start_dialog
from app.settings import settings
from app.main import app


logger = logging.getLogger(__name__)

# Установка middleware и роутеров для бота
dp.update.middleware(DbSessionMiddleware(sessionmaker=db_helper.sessionmaker))
dp.include_routers(start_dialog)
setup_dialogs(dp)


# Функция для запуска бота
async def start_bot():
    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s "
               "[%(asctime)s] - %(name)s - %(message)s",
    )
    logger.info("Starting bot")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

# Функция для запуска FastAPI и бота
async def main():
    # Запуск бота в фоне
    asyncio.create_task(start_bot())

    # Запуск FastAPI приложения
    config = uvicorn.Config(
        "app.main:app", 
        host=settings.api.host,
        port=settings.api.port,
        log_level="info",
        reload=True,
    )
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt as exxit:
        logger.info(f"Бот закрыт: {exxit}")
