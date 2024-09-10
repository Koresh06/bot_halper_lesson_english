from datetime import datetime, date, time
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Result, desc

from app.core.models import User


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


    async def get_user_id(self, user_id: int) -> int:
        stmt = select(User.tg_id).where(User.id == user_id)
        result: Result = await self.session.scalar(stmt)
        return result

    async def get_profile(self, user_id) -> User:
        stmt = select(User).where(User.id == user_id)
        result: Result = await self.session.scalar(stmt)
        return result

    async def get_users_tg_id(self) -> List[User]:
        stmt = select(User.tg_id).order_by(desc(User.id))
        result: Result = await self.session.scalars(stmt)
        return result


    
    
    

        
