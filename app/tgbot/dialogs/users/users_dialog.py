from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram_dialog import Dialog, DialogManager, StartMode, Window
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.input import TextInput, ManagedTextInput
from aiogram_dialog.widgets.kbd import Button, Next

from tgbot.bot import dp
from tgbot.dialogs.users.getters import username_getter
from tgbot.dialogs.users.states import StartSG
from tgbot.dialogs.users.handlers import correct_age_handler, correct_name_handler, error_age_handler, error_name_handler
from tgbot.dialogs.users.utils import age_check, name_check





start_dialog = Dialog(
    Window(
        Format(text='Привет, {username}!', when="new_user"),
        Format(text='Вы не новый пользователь, {username}!', when="not_new_user"),
        Next(Const(text="Пройти опрос ▶"), id="start_survey", when="not_new_user"),
        getter=username_getter,
        state=StartSG.start
    ),
    Window(
        Const(text="Укажите как к вам обращаться"),
        TextInput(
            id='name_input',
            type_factory=name_check,
            on_success=correct_name_handler,
            on_error=error_name_handler,
        ),
        state=StartSG.name,
    ),
    Window(
        Const(text='Введите ваш возраст'),
        TextInput(
            id='age_input',
            type_factory=age_check,
            on_success=correct_age_handler,
            on_error=error_age_handler,
        ),
        state=StartSG.age,
    )
)


@dp.message(CommandStart())
async def command_start_process(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(state=StartSG.start, mode=StartMode.RESET_STACK)