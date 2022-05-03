from dataclasses import dataclass

from app.configs.database import db
from sqlalchemy import Column, ForeignKey, Integer, String


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
