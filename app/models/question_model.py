from dataclasses import dataclass

from app.configs.database import db
<<<<<<< HEAD
from sqlalchemy import VARCHAR, Column, ForeignKey, BigInteger, Integer
=======
from sqlalchemy import VARCHAR, Column, ForeignKey, Integer
from sqlalchemy.orm import relationship, backref
>>>>>>> 21637a784c00a144ca927e87be3a6d70f88211e3

@dataclass
class QuestionModel(db.Model):
    __tablename__ = 'questions'

    id: int
<<<<<<< HEAD
    question: str
    product_id: int
    parent_id: int
=======
    question: str 
>>>>>>> 21637a784c00a144ca927e87be3a6d70f88211e3

    id = Column(BigInteger, primary_key=True)
    question = Column(VARCHAR(2200), nullable=False)

    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    parent_id = Column(Integer, ForeignKey('parents.cpf'), nullable=False)

    answer = relationship(
        "AswerModel",
        backref=backref(
            "question",
            uselist=False
        ), uselist=False
    )