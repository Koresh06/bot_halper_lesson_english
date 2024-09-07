from sched import scheduler
from typing import Annotated
from fastapi import APIRouter, Form, Request, Depends, status
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date, datetime, time, timedelta

from app.core.db_helper import db_helper
from app.tgbot.api.service import UsersService
from app.core.models import Lesson
from app.tgbot.api.utils import send_lesson_notification
from .schemas.lesson_schemas import LessonCreateSchema
from app.tgbot.config import templates


router = APIRouter(
    prefix="/lessons",
    tags=["lessons"],
    responses={
        404: {"description": "Not found"},
    },
)


# Отображение списка уроков
@router.get("/get-lessons", response_class=HTMLResponse)
async def get_lessons_page(
    request: Request,
    session: Annotated[
        AsyncSession,
        Depends(db_helper.get_db),
    ],
):
    lessons = await UsersService(session).get_lessons()

    return templates.TemplateResponse(
        "home.html",
        {
            "request": request,
            "lessons": lessons,
        },
    )


# Получение списка пользователей
@router.get("/create-lesson", response_class=HTMLResponse)
async def get_create_lesson_page(
    request: Request,
    session: Annotated[
        AsyncSession,
        Depends(db_helper.get_db),
    ],
):
    users = await UsersService(session).get_users()

    return templates.TemplateResponse(
        "create_lesson.html",
        {
            "request": request,
            "users": users,
        },
    )


# Обработка данных из формы и создание урока
@router.post("/submit-lesson")
async def submit_lesson(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.get_db),
    ],
    create_lesson_form: LessonCreateSchema = Depends(LessonCreateSchema.as_form),
):
    lesson = await UsersService(session).create_lesson(
        user_id=create_lesson_form.user_id,
        lesson_date=create_lesson_form.lesson_date,
        lesson_time=create_lesson_form.lesson_time,
    )
    user_tg_id = await UsersService(session).get_user_id(
        user_id=create_lesson_form.user_id
    )

    await send_lesson_notification(
        tg_id=user_tg_id,
        lesson_date=lesson.lesson_date,
        lesson_time=lesson.lesson_time,
    )

    return RedirectResponse(url="/lessons/get-lessons", status_code=status.HTTP_302_FOUND)


@router.get("/delete-lesson/{lesson_id}")
async def delete_lesson(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.get_db),
    ],
    lesson_id: int,
):
    await UsersService(session).delete_lesson(lesson_id=lesson_id)
    return RedirectResponse(url="/lessons/get-lessons", status_code=status.HTTP_302_FOUND)


# @router.post("/edit-lesson/{lesson_id}")
# async def edit_lesson(
#     session: Annotated[
#         AsyncSession,
#         Depends(db_helper.get_db),
#     ],
#     lesson_id: int,
# ):
#     lesson = await UsersService(session).get_lesson(lesson_id=lesson_id)
#     return RedirectResponse(url="/lessons/get-lessons", status_code=status.HTTP_302_FOUND)
