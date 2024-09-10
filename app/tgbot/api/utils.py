import asyncio
from datetime import date, time
from aiogram.enums.parse_mode import ParseMode

from app.tgbot.bot import bot
from app.settings import settings


async def send_lesson_notification(
    tg_id: int,
    lesson_date: date,
    lesson_time: time,
) -> None:
    message = (
        f"<b>Вы записаны на урок!</b>\n\n"
        f"🗓 <b>Дата:</b> {lesson_date.strftime('%Y-%m-%d')}\n"
        f"⏰ <b>Время:</b> {lesson_time.strftime('%H:%M')}\n\n"
        f"<i>Спасибо, что используете наш сервис!</i>"
    )
    
    await bot.send_message(
        chat_id=tg_id,
        text=message,
        parse_mode=ParseMode.HTML
    )


async def send_newletter_notification(tg_ids: list, message: str) -> None:
    for id in tg_ids:
        await bot.send_message(
            chat_id=id,
            text=message
        )

    await bot.send_message(chat_id=settings.bot.admin_id, text="Рассылка завершена успешно")
    
    
