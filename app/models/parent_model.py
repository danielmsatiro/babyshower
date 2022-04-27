from sqlalchemy import Column, Integer, String, ForeignKey, BigInteger
from dataclasses import dataclass
from app.configs.database import db
from sqlalchemy.orm import relationship, backref
from werkzeug.security import check_password_hash, generate_password_hash


@dataclass
class ParentModel(db.Model):

    __tablename__ = "parents"

    cpf: str
    username: str
    email: str
    name: str
    phone: str
    password_hash: str

    id = Column(Integer, primary_key=True, nullable=False)
    cpf = Column(String, nullable=False, unique=True)
    username = Column(String, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    
    products = relationship(
        'ProductModel',
        backref=backref('parent', uselist=False)
    )

    questions = relationship(
        'QuestionModel', 
        backref=backref('parent', uselist=False)
    )

    @property
    def password(self):
        raise AttributeError("Password cannot be accessed")
    
    @password.setter
    def password(self, password_to_hash):
        self.password_hash = generate_password_hash(password_to_hash)

    def verify_password(self, password_to_compare):
        return check_password_hash(self.password_hash, password_to_compare)