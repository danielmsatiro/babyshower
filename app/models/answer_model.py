from dataclasses import dataclass
from datetime import datetime as dt

from app.configs.database import db
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String


@dataclass
class AnswerModel(db.Model):
    id: int
    answer: str
    created_at: dt
    updated_at: dt
    parent_id: int
    question_id: int

    __tablename__ = "answers"

    id = Column(Integer, primary_key=True)
    answer = Column(String(150), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    parent_id = Column(ForeignKey("parents.id", ondelete="CASCADE"), nullable=False)
    question_id = Column(
        ForeignKey("questions.id", ondelete="CASCADE"), nullable=False, unique=True
    )
