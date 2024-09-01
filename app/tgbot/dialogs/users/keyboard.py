from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup 

async def new_user(tg_id, name):
    builder = InlineKeyboardBuilder()

    builder.add(InlineKeyboardButton(text=f'🔶 {name}',url=f'tg://user?id={tg_id}'))
    return builder.as_markup()