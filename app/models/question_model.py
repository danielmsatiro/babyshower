from dataclasses import dataclass

from app.configs.database import db
from sqlalchemy import VARCHAR, Column, ForeignKey, Integer
from sqlalchemy.orm import relationship, backref

@dataclass
class QuestionModel(db.Model):
    __tablename__ = 'questions'

    id: int
    question: str 

    id = Column(Integer, primary_key=True)
    question = Column(VARCHAR(2200), nullable=False)

    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    parent_id = Column(Integer, ForeignKey('parents.cpf'), nullable=False)

    answer = relationship(
        "AnswerModel",
        backref=backref(
            "question",
            uselist=False
        ), uselist=False
    )