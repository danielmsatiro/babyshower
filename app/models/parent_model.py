from sqlalchemy import Column, Integer, String
from dataclasses import dataclass
from sqlalchemy.sql.schema import UniqueConstraint
from app.configs.database import db

from sqlalchemy.orm import relationship, backref

@dataclass
class ParentModel(db.Model):

    __tablename__ = "parents"

    cpf: int

    cpf = Column(Integer, primary_key=True, nullable=False)
    username: str = Column(String, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    

    # c = relationship(
        #     '',
        #     secondary='',
        #     backref=backref('')
        # )
    
    questions = relationship(
        'QuestionModel', 
        backref=backref('parent')
    )