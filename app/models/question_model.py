from dataclasses import dataclass

from app.configs.database import db
from sqlalchemy import String, Column, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship, backref

@dataclass
class QuestionModel(db.Model):
    __tablename__ = 'questions'

    id: int
    question: str
    product_id: int
    parent_id: int
    answer: str

    id = Column(Integer, primary_key=True, nullable=False)
    question = Column(Text, nullable=False)

    product_id = Column(Integer, ForeignKey('products.id', ondelete="CASCADE"), nullable=False)
    parent_id = Column(Integer, ForeignKey('parents.id', ondelete="CASCADE"), nullable=False)

    answer = relationship(
        "AnswerModel",
        backref=backref(
            "question",
            uselist=False
        ), uselist=False
    )
