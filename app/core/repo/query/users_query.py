from typing import Optional

from sqlalchemy import select, Result
from app.core.models import User

from app.core.repo.base import BaseRepo


class UserRepo(BaseRepo):


    async def check_user(self, tg_id: int):
        user = await self.session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            return True
        return False


    async def add_user(self, tg_id: int, username: str, data: dict):
        try:
            new_user = User(
                tg_id=tg_id,
                username=data.get("username"),
                name=data.get("name"),
                age=int(data.get("age")),
                phone=data.get("phone"),
                study_goal=data.get("study_goal"),
                has_studied_before=data.get("has_studied_before"),
                study_format=data.get("study_format"),
                training_format=data.get("training_format"),
            )
            self.session.add(new_user)
            await self.session.commit()
            await self.session.refresh(new_user)
            return new_user 
        except Exception as ex:
            await self.session.rollback()
            print(f"Ошибка при добавлении пользователя: {ex}")
