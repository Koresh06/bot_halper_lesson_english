from typing import Annotated
from fastapi import APIRouter, Form, Request, Depends, status
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date, datetime, time, timedelta

from app.core.db_helper import db_helper
from app.tgbot.api.service.user_service import UsersService
from app.tgbot.config import templates


router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={
        404: {"description": "Not found"},
    },
)


@router.get("/profile/{user_id}", response_class=HTMLResponse)
async def get_user(
    request: Request,
    session: Annotated[
        AsyncSession,
        Depends(db_helper.get_db),
    ],
    user_id: int,
):
    try:
        user = await UsersService(session).get_profile(user_id)
    except Exception as exx:
        print(exx)

    return templates.TemplateResponse(
        "profile.html",
        {
            "request": request,
            "user": user,
        },
    )


@router.get("/get-users", response_class=HTMLResponse)
async def get_users(
    request: Request,
    session: Annotated[
        AsyncSession,
        Depends(db_helper.get_db),
    ],
):
    try:
        users = await UsersService(session).get_users()
    except Exception as exx:
        print(exx)

    return templates.TemplateResponse(
        "users.html",
        {
            "request": request,
            "users": users,
        },
    )