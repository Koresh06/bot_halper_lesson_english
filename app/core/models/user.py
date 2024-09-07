from typing import TYPE_CHECKING
from enum import Enum as PyEnum
from sqlalchemy import BigInteger, Enum, String, Integer, Boolean, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.models.base import Base

if TYPE_CHECKING:
    from app.core.models import Lesson


class StudyFormatEnum(PyEnum):
    ONLINE = "online"
    OFFLINE = "offline"

class TrainingFormatEnum(PyEnum):
    GROUP = "group"
    PAIR = "pair"
    INDIVIDUAL = "individual"


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    study_goal: Mapped[str] = mapped_column(Text, nullable=False) 
    has_studied_before: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    study_format: Mapped[StudyFormatEnum] = mapped_column(Enum(StudyFormatEnum), nullable=False)
    training_format: Mapped[TrainingFormatEnum] = mapped_column(Enum(TrainingFormatEnum), nullable=False)

    lesson_rel: Mapped[list["Lesson"]] = relationship("Lesson", back_populates="user_rel", cascade="all, delete")

    def __repr__(self) -> str:
        return (
            f"<User(name={self.name}, age={self.age}, goal={self.study_goal[:50]}..., "
            f"studied_before={self.has_studied_before}, format={self.study_format.value})>"
        )