from datetime import date, time, datetime
from typing import TYPE_CHECKING
from sqlalchemy import BigInteger, Boolean, DateTime, ForeignKey, Date, String, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.models.base import Base

if TYPE_CHECKING:
    from app.core.models import User


class Lesson(Base):
    __tablename__ = 'lessons'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    lesson_date: Mapped[date] = mapped_column(Date, nullable=False)
    lesson_time: Mapped[time] = mapped_column(Time, nullable=False)
    reminder_sent: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)

    user_rel: Mapped["User"] = relationship("User", back_populates="lesson_rel")

    def __repr__(self) -> str:
        return (f"<Lesson(user_id={self.user_id}, lesson_date={self.lesson_date}, "
                f"lesson_time={self.lesson_time}, reminder_sent={self.reminder_sent})>")