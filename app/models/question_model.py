from dataclasses import dataclass

from app.configs.database import db
<<<<<<< HEAD
from sqlalchemy import VARCHAR, Column, ForeignKey, Integer
=======
from sqlalchemy import String, Column, ForeignKey, Integer, Text
>>>>>>> development
from sqlalchemy.orm import relationship, backref

@dataclass
class QuestionModel(db.Model):
    __tablename__ = 'questions'

    id: int
    question: str
    product_id: int
    parent_id: int

    id = Column(Integer, primary_key=True)
    question = Column(Text, nullable=False)

    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    parent_id = Column(Integer, ForeignKey('parents.id'), nullable=False)

    answer = relationship(
        "AnswerModel",
        backref=backref(
            "question",
            uselist=False
        ), uselist=False
    )
