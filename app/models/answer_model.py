from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import backref, relationship
from dataclasses import dataclass

from app.configs.database import db
from app.models.parent_model import ParentModel
from app.models.question_model import QuestionModel


@dataclass
class AnswerModel(db.Model):
    id: int
    answer: str
    parent_id: int
    question_id: int

    __tablename__ = "answers"

    id = Column(Integer, primary_key=True)
    answer = Column(String(150), nullable=False)

    parent_id = Column(ForeignKey("parents.id", ondelete="CASCADE"), nullable=False)

    question_id = Column(
        ForeignKey("questions.id", ondelete="CASCADE"), nullable=False, unique=True
    )

    # parent = relationship(
    #     "ParentModel",
    #     backref=backref(
    #         "answer",
    #         uselist=False
    #     ), uselist=False
    # )
