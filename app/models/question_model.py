from dataclasses import dataclass

from app.configs.database import db
from sqlalchemy import VARCHAR, Column, ForeignKey, BigInteger, Integer

@dataclass
class QuestionModel(db.Model):
    __tablename__ = 'questions'

    id: int
    question: str
    product_id: int
    parent_id: int

    id = Column(BigInteger, primary_key=True)
    question = Column(VARCHAR(2200), nullable=False)

    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    parent_id = Column(Integer, ForeignKey('parents.cpf'), nullable=False)