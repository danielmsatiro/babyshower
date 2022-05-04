from dataclasses import dataclass
from datetime import datetime as dt

from app.configs.database import db
from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text
from sqlalchemy.orm import backref, relationship


@dataclass
class QuestionModel(db.Model):
    __tablename__ = "questions"

    id: int
    question: str
    created_at: dt
    updated_at: dt
    product_id: int
    parent_id: int
    answer: str

    id = Column(Integer, primary_key=True, nullable=False)
    question = Column(Text, nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    product_id = Column(
        Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False
    )
    parent_id = Column(
        Integer, ForeignKey("parents.id", ondelete="CASCADE"), nullable=False
    )

    answer = relationship(
        "AnswerModel", backref=backref("question", uselist=False), uselist=False
    )
