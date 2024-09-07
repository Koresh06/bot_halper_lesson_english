from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.enums import ContentType
from aiogram_dialog import Dialog, DialogManager, StartMode, Window
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.input import TextInput, MessageInput
from aiogram_dialog.widgets.kbd import Button, Next, Row, Calendar
from app.tgbot.bot import dp



lessons_dialog = Dialog(
    Window(

    )
)