from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.enums import ContentType
from aiogram_dialog import Dialog, DialogManager, StartMode, Window
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.input import TextInput, MessageInput
from aiogram_dialog.widgets.kbd import Button, Next, Row, Back, Url
from app.tgbot.bot import dp
from app.settings import settings
from app.tgbot.dialogs.users.getters import username_getter
from app.tgbot.dialogs.users.states import StartSG
from app.tgbot.dialogs.users.handlers import (
    correct_age_handler,
    correct_name_handler,
    correct_phone_handler,
    correct_study_goal_handler,
    error_age_handler,
    error_name_handler,
    error_phone_handler,
    error_study_goal_handler,
    has_studied_before_handler,
    study_format_handler,
    training_handler,
)
from app.tgbot.dialogs.users.utils import (
    age_check,
    study_goal_check,
    name_check,
    phone_check,
)


start_dialog = Dialog(
    Window(
        Format("Привет, {username}!", when="new_user"),
        Format("Вы новый пользователь, {username}!", when="not_new_user"),
        Next(
            Const(text="Пройти опрос ▶"),
            id="start_survey",
            when="not_new_user",
        ),
        Url(
            text=Const("🔰 Панель администратора"),
            url=Const(settings.api.web_server_admin),
            id="admin_panel",
            when="check_admin",
        ),
        getter=username_getter,
        state=StartSG.start,
    ),
    Window(
        Const(text="Укажите как к вам обращаться"),
        TextInput(
            id="name_input",
            type_factory=name_check,
            on_success=correct_name_handler,
            on_error=error_name_handler,
        ),
        Back(Const("◀️ Назад"), id="back"),
        state=StartSG.name,
    ),
    Window(
        Const(text="Введите ваш возраст"),
        TextInput(
            id="age_input",
            type_factory=age_check,
            on_success=correct_age_handler,
            on_error=error_age_handler,
        ),
        Back(Const("◀️ Назад"), id="back"),
        state=StartSG.age,
    ),
    Window(
        Const(text="Напишите свой номер телефона"),
        TextInput(
            id="phone_input",
            type_factory=phone_check,
            on_success=correct_phone_handler,
            on_error=error_phone_handler,
        ),
        Back(Const("◀️ Назад"), id="back"),
        state=StartSG.phone,
    ),
    Window(
        Const(text="Опишите свою цель обучения"),
        TextInput(
            id="study_format_input",
            type_factory=study_goal_check,
            on_success=correct_study_goal_handler,
            on_error=error_study_goal_handler,
        ),
        Back(Const("◀️ Назад"), id="back"),
        state=StartSG.study_goal,
    ),
    Window(
        Const(text="Изучали язык раньше?"),
        Row(
            Button(
                Const("✅ Да"),
                id="yes",
                on_click=has_studied_before_handler,
            ),
            Button(
                Const("❌ Нет"),
                id="no",
                on_click=has_studied_before_handler,
            ),
        ),
        Back(Const("◀️ Назад"), id="back"),
        state=StartSG.has_studied_before,
    ),
    Window(
        Const(text="Укажите предпочитаемый формат обучения"),
        Row(
            Button(
                Const("Онлайн"),
                id="online",
                on_click=study_format_handler,
            ),
            Button(
                Const("Оффлайн"),
                id="offline",
                on_click=study_format_handler,
            ),
        ),
        Back(Const("◀️ Назад"), id="back"),
        state=StartSG.study_format,
    ),
    Window(
        Const(text="Как вы хотите обучаться?"),
        Row(
            Button(
                Const("Гупповое"),
                id="group",
                on_click=training_handler,
            ),
            Button(
                Const("Парное"),
                id="pair",
                on_click=training_handler,
            ),
            Button(
                Const("Индивидуальное"),
                id="individual",
                on_click=training_handler,
            ),
        ),
        Back(Const("◀️ Назад"), id="back"),
        state=StartSG.training_format,
    ),
)


@dp.message(CommandStart())
async def command_start_process(callback: CallbackQuery, dialog_manager: DialogManager):
    await dialog_manager.start(state=StartSG.start, mode=StartMode.RESET_STACK)
