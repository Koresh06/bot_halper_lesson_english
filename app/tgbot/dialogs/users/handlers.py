from aiogram.types import Message
from aiogram_dialog.widgets.input import ManagedTextInput
from aiogram_dialog import DialogManager



# Хэндлер, который сработает, если пользователь ввел корректный имени
async def correct_name_handler(
        message: Message, 
        widget: ManagedTextInput, 
        dialog_manager: DialogManager, 
        text: str) -> None:
    
    await message.answer(text=f'Ваше имя {text}')
    await dialog_manager.next()


# Хэндлер, который сработает на ввод некорректного имени
async def error_name_handler(
        message: Message, 
        widget: ManagedTextInput, 
        dialog_manager: DialogManager, 
        error: ValueError):
    await message.answer(
        text='Вы ввели некорректное имя. Попробуйте еще раз\n\nТребования к имени:\n1.Имя должно содержать только буквы и пробелы\n2. Длина имени от 1 до 50 символов\n3. Начинается с заглавной буквы\n'
    )


# Хэндлер, который сработает, если пользователь ввел корректный возраст
async def correct_age_handler(
        message: Message, 
        widget: ManagedTextInput, 
        dialog_manager: DialogManager, 
        text: str) -> None:
    
    await message.answer(text=f'Вам {text}')
    await dialog_manager.done()


# Хэндлер, который сработает на ввод некорректного возраста
async def error_age_handler(
        message: Message, 
        widget: ManagedTextInput, 
        dialog_manager: DialogManager, 
        error: ValueError):
    await message.answer(
        text='Вы ввели некорректный возраст. Попробуйте еще раз'
    )