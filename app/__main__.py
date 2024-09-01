import asyncio
import logging

from aiogram_dialog import setup_dialogs
from app.core.session import create_engine_db, create_sessionmaker
from app.tgbot.middlewares.db_session import DbSessionMiddleware

from app.tgbot.bot import dp, bot
from app.tgbot.dialogs.users.users_dialog import start_dialog

from app.settings import settings


logger = logging.getLogger(__name__)


engine = create_engine_db(settings.db)
sessionmaker = create_sessionmaker(engine)

dp.update.middleware(DbSessionMiddleware(sessionmaker=sessionmaker))

dp.include_routers(start_dialog)

setup_dialogs(dp)

# Функция для запуска бота
async def start_bot():
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s'
    )
    logger.info('Staring bot')
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    

if __name__ == '__main__':
    try:
        asyncio.run(start_bot())
    except KeyboardInterrupt as exxit:
        logger.info(f'Бот закрыт: {exxit}')