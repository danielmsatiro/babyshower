from dataclasses import dataclass

from app.configs.database import db
from sqlalchemy import VARCHAR, Column, ForeignKey, Integer

@dataclass
class QuestionModel(db.Model):
    __tablename__ = 'questions'

    id: int
    question: str

    id = Column(Integer, primary_key=True)
    question = Column(VARCHAR, nullable=False)

    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    parent_id = Column(Integer, ForeignKey('parents.id'), nullable=False)