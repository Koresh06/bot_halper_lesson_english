from aiogram_dialog import DialogManager
from aiogram.types import User

from core.repo.requests import RequestsRepo


async def username_getter(
    repo: RequestsRepo,
    dialog_manager: DialogManager,
    event_from_user: User,
    **kwargs,
):
    user = await repo.users.check_user(event_from_user.id)
    if user:
        try:
            await repo.users.add_user(event_from_user.id)
        except Exception as ex:
            print(ex)

    return {
        "username": event_from_user.username,
        "new_user": not user,
        "not_new_user": user,
    }
