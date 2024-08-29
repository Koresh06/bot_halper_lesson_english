from typing import Optional

from sqlalchemy import select, Result
from core.models import User

from core.models.user import StudyFormatEnum
from core.repo.base import BaseRepo


class UserRepo(BaseRepo):


    async def check_user(self, tg_id: int):
        user = await self.session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            return True
        return False


    async def add_user(self, tg_id: int):
        pass
        # new_user = User(
        #     tg_id=tg_id,
        #     username="john_doe",
        #     name="John Doe",
        #     age=30,
        #     phone="1234567890",
        #     study_goal="Improve English skills",
        #     has_studied_before=True,
        #     study_format=StudyFormatEnum.ONLINE,
        # )
        # self.session.add(new_user)
        # await self.session.commit()
        # await self.session.refresh(new_user)
