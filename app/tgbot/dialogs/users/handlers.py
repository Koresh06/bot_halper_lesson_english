from typing import Any
from aiogram.types import Message, CallbackQuery, User
from aiogram_dialog.widgets.input import ManagedTextInput
from aiogram_dialog import DialogManager

from app.core.repo.requests import RequestsRepo
from app.core.models.user import StudyFormatEnum, TrainingFormatEnum
from app.settings import settings

from app.tgbot.dialogs.users.keyboard import new_user

# Хэндлер, который сработает, если пользователь ввел корректный имени
async def correct_name_handler(
    message: Message, widget: ManagedTextInput, dialog_manager: DialogManager, text: str
) -> None:

    await message.answer(text=f"Ваше имя {text}")
    dialog_manager.dialog_data.update({"name": text})
    await dialog_manager.next()


# Хэндлер, который сработает на ввод некорректного имени
async def error_name_handler(
    message: Message,
    widget: ManagedTextInput,
    dialog_manager: DialogManager,
    error: ValueError,
):
    await message.answer(
        text="Вы ввели некорректное имя. Попробуйте еще раз\n\nТребования к имени:\n1.Имя должно содержать только буквы и пробелы\n2. Длина имени от 1 до 50 символов\n3. Начинается с заглавной буквы\n"
    )


# Хэндлер, который сработает, если пользователь ввел корректный возраст
async def correct_age_handler(
    message: Message, widget: ManagedTextInput, dialog_manager: DialogManager, text: str
) -> None:

    await message.answer(text=f"Вам {text}")
    dialog_manager.dialog_data.update({"age": text})
    await dialog_manager.next()


# Хэндлер, который сработает на ввод некорректного возраста
async def error_age_handler(
    message: Message,
    widget: ManagedTextInput,
    dialog_manager: DialogManager,
    error: ValueError,
):
    await message.answer(text="Вы ввели некорректный возраст. Попробуйте еще раз")


# Хэндлер, который сработает, если пользователь ввел корректный номер телефона
async def correct_phone_handler(
    message: Message, widget: ManagedTextInput, dialog_manager: DialogManager, text: str
) -> None:

    await message.answer(text=f"Ваш номер телефона {text}")
    dialog_manager.dialog_data.update({"phone": text})
    await dialog_manager.next()


# Хэндлер, который сработает на ввод некорректного номер телефона
async def error_phone_handler(
    message: Message,
    widget: ManagedTextInput,
    dialog_manager: DialogManager,
    error: ValueError,
):
    await message.answer(
        text="Вы ввели некорректный номер телефона. Попробуйте еще раз"
    )


# Хэндлер, который сработает, если пользователь ввел некорректную цель обучения
async def correct_study_goal_handler(
    message: Message, widget: ManagedTextInput, dialog_manager: DialogManager, text: str
) -> None:

    await message.answer(text=f"Ваш цель {text}")
    dialog_manager.dialog_data.update({"study_goal": text})
    await dialog_manager.next()


# Хэндлер, который сработает на ввод некорректной цели обучения
async def error_study_goal_handler(
    message: Message,
    widget: ManagedTextInput,
    dialog_manager: DialogManager,
    error: ValueError,
):
    await message.answer(text="Вы ввели некорректная цель обучения. Попробуйте еще раз")


async def has_studied_before_handler(
    callback: CallbackQuery, widget: ManagedTextInput, dialog_manager: DialogManager
) -> None:
    has_studied_before = callback.data

    if has_studied_before == "yes":
        dialog_manager.dialog_data.update({"has_studied_before": True})
    elif has_studied_before == "no":
        dialog_manager.dialog_data.update({"has_studied_before": False})
    else:
        await callback.message.answer(text="Некорректный выбор.")
        return

    await dialog_manager.next()


async def study_format_handler(
    callback: CallbackQuery,
    widget: Any,
    dialog_manager: DialogManager,
):
    study_format = callback.data

    if study_format == StudyFormatEnum.ONLINE.value:
        dialog_manager.dialog_data.update({"study_format": StudyFormatEnum.ONLINE})
    elif study_format == StudyFormatEnum.OFFLINE.value:
        dialog_manager.dialog_data.update({"study_format": StudyFormatEnum.OFFLINE})
    else:
        await callback.message.answer(text="Некорректный формат обучения.")
        return

    await dialog_manager.next()


async def training_handler(
    callback: CallbackQuery,
    widget: Any,
    dialog_manager: DialogManager,
):
    repo: RequestsRepo = dialog_manager.middleware_data.get("repo")

    training_format = callback.data

    if training_format == TrainingFormatEnum.GROUP.value:
        dialog_manager.dialog_data.update({"training_format": TrainingFormatEnum.GROUP})
    elif training_format == TrainingFormatEnum.PAIR.value:
        dialog_manager.dialog_data.update({"training_format": TrainingFormatEnum.PAIR})
    elif training_format == TrainingFormatEnum.INDIVIDUAL.value:
        dialog_manager.dialog_data.update(
            {"training_format": TrainingFormatEnum.INDIVIDUAL}
        )
    else:
        await callback.message.answer(text="Некорректный формат тренировки.")
        return

    await repo.users.add_user(
        tg_id=callback.from_user.id,
        username=callback.from_user.username,
        data=dialog_manager.dialog_data,
    )

    data = dialog_manager.dialog_data

    await callback.message.bot.send_message(
        chat_id=settings.bot.admin_ids,
        text=(
            f"👤 *Новый пользователь:*\n"
            f"   — Имя: *{data['name']}*\n"
            f"   — Возраст: *{data['age']}*\n"
            f"   — ☎️ Телефон: *{data['phone']}*\n\n"
            f"🎯 *Цель обучения:*\n"
            f"   — *{data['study_goal']}*\n\n"
            f"📚 *Формат обучения:*\n"
            f"   — *{data['study_format'].value}*\n"
            f"🏋️ *Вид тренировки:*\n"
            f"   — *{data['training_format'].value}*" 
        ),
        parse_mode="Markdown",
        reply_markup=await new_user(
            tg_id=callback.from_user.id,
            name=data["name"],
        )
    )

    await dialog_manager.done()
    await callback.message.answer(text="Спасибо за заявку. Ожидайте звонка")
