from typing import Annotated
from fastapi import APIRouter, Form, Request, Depends, status
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date, datetime, time, timedelta

from app.core.db_helper import db_helper
from app.tgbot.api.service.lesson_service import LessonsService
from app.tgbot.api.service.user_service import UsersService
from app.tgbot.api.utils import send_lesson_notification
from ..schemas.lesson_schemas import LessonCreateSchema, EditLessonSchema
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
    try:
        lessons = await LessonsService(session).get_lessons()
    except Exception as exx:
        print(exx)

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
    try:
        users = await UsersService(session).get_users()
    except Exception as exx:
        print(exx)

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
    try:
        lesson = await LessonsService(session).create_lesson(
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

    except Exception as exx:
        print(exx)
        
    return RedirectResponse(url="/lessons/get-lessons", status_code=status.HTTP_302_FOUND)


@router.get("/delete-lesson/{lesson_id}")
async def delete_lesson(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.get_db),
    ],
    lesson_id: int,
):
    try:
        await LessonsService(session).delete_lesson(lesson_id=lesson_id)
    except Exception as exx:
        print(exx)

    return RedirectResponse(url="/lessons/get-lessons", status_code=status.HTTP_302_FOUND)


@router.get("/edit-lesson/{lesson_id}", response_class=HTMLResponse)
async def edit_lesson_page(
    request: Request,
    session: Annotated[
        AsyncSession,
        Depends(db_helper.get_db),
    ],
    lesson_id: int,
):
    try:
        lesson = await LessonsService(session).get_lesson(lesson_id=lesson_id)
        users = await UsersService(session).get_users()
    except Exception as exx:
        print(exx)

    return templates.TemplateResponse(
        "edit_lesson.html",
        {
            "request": request,
            "lesson": lesson,
            "users": users,
        },
    )
    

@router.post("/edit-lesson/{lesson_id}")
async def edit_lesson(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.get_db),
    ],
    lesson_id: int,
    edit_lesson_form: EditLessonSchema = Depends(EditLessonSchema.as_form),
):
    try:
        await LessonsService(session).edit_lesson(
            lesson_id=lesson_id,
            user_id=edit_lesson_form.user_id,
            lesson_date=edit_lesson_form.lesson_date,
            lesson_time=edit_lesson_form.lesson_time,
        )
    except Exception as exx:
        print(exx)
    return RedirectResponse(url="/lessons/get-lessons", status_code=status.HTTP_302_FOUND)
