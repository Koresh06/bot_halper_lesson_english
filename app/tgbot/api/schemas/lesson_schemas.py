from datetime import date, time
from typing import Annotated
from pydantic import BaseModel
from fastapi import Form


class LessonCreateSchema(BaseModel):
    user_id: int
    lesson_date: date
    lesson_time: time

    @classmethod
    def as_form(
        cls,
        user_id: int = Form(...),
        lesson_date: date = Form(...),
        lesson_time: time = Form(...),
    ):
        return cls(
            user_id=user_id,
            lesson_date=lesson_date,
            lesson_time=lesson_time,
        )
