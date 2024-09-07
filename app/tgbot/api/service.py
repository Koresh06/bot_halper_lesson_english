from datetime import datetime, date, time
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Result, desc

from app.core.models import User, Lesson


class UsersService:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_users(self) -> List[User]:
        stmt = select(User).order_by(desc(User.id))
        result: Result = await self.session.scalars(stmt)
        return result

    async def get_user(self, tg_id: int) -> User:
        stmt = select(User).where(User.tg_id == tg_id)
        result: Result = await self.session.scalars(stmt)
        return result.first()

    async def create_lesson(
        self,
        user_id: int,
        lesson_date: date,
        lesson_time: time,
    ) -> Lesson:
        new_lesson = Lesson(
            user_id=user_id,
            lesson_date=lesson_date,
            lesson_time=lesson_time,
        )
        self.session.add(new_lesson)
        await self.session.commit()
        return new_lesson

    async def get_user_id(self, user_id: int) -> int:
        stmt = select(User.tg_id).where(User.id == user_id)
        result: Result = await self.session.scalar(stmt)
        return result

    async def get_lessons(self) -> List[dict]:
        stmt = select(Lesson, User.username).join(User, Lesson.user_id == User.id)
        result = await self.session.execute(stmt)
        lessons = result.fetchall()

        return [
            {
                "id": lesson.id,
                "user_id": lesson.user_id,
                "username": username,
                "lesson_date": lesson.lesson_date,
                "lesson_time": lesson.lesson_time,
                "reminder_sent": lesson.reminder_sent,
            }
            for lesson, username in lessons
        ]
    
    async def delete_lesson(self, lesson_id: int):
        stmt = select(Lesson).where(Lesson.id == lesson_id)
        result: Result = await self.session.scalar(stmt)

        await self.session.delete(result)
        await self.session.commit()
