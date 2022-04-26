from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import backref, relationship
from dataclasses import dataclass

from app.models.parent_model import ParentModel
from app.models.question_model import QuestionModel

@dataclass
class AnswerModel():
    id = int
    answer = str
    parent = ParentModel
    question = QuestionModel

    __tablename__ = "answers"

    id = Column(Integer, primary_key=True)
    answer = Column(String(150))

    parent_id = Column(
        ForeignKey('parents.id'),
        nullable=False,
        unique=True
    )

    question_id = Column(
        ForeignKey('questions.id'),
        nullable=False,
        unique=True
    )

    parent = relationship(
        "ParentModel",
        backref=backref(
            "answer",
            use_list=False
        )
    )
