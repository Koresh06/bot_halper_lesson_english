from collections.abc import Awaitable
import logging
from typing import Any, Callable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from core.repo.requests import RequestsRepo


logger = logging.getLogger(__name__)


class DbSessionMiddleware(BaseMiddleware):
    def __init__(self,sessionmaker: async_sessionmaker[AsyncSession]) -> None:
        super().__init__()
        self.sessionmaker = sessionmaker

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any]
    ) -> Any:
        async with self.sessionmaker() as session:
            repo = RequestsRepo(session)
            data["repo"] = repo
            data["session"] = session
            logger.info(f"Repo added to data: {repo}")
            result = await handler(event, data)
        return result