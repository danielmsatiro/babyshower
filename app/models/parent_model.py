from dataclasses import dataclass

from app.configs.database import db
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import backref, relationship
from werkzeug.security import check_password_hash, generate_password_hash


@dataclass
class ParentModel(db.Model):

    __tablename__ = "parents"

    id: int
    cpf: str
    username: str
    email: str
    name: str
    phone: str

    id = Column(Integer, primary_key=True, nullable=False)
    cpf = Column(String, nullable=False, unique=True)
    username = Column(String, nullable=False, unique=True)
    name: str = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password_hash = Column(String, nullable=False)
    phone = Column(String, nullable=False)

    nome_municipio: str = Column(String, nullable=False)
    estado: str = Column(String, nullable=False)

    # remover columns nome_municipio e estado
    # adicionar column point_id

    # products = relationship(
    # "ProductModel", backref=backref(
    # "parent", passive_deletes=True, uselist=False))

    # questions = relationship(
    # "QuestionModel", backref=backref(
    # "parent", passive_deletes=True, uselist=False))

    @property
    def password(self):
        raise AttributeError("Password cannot be accessed")

    @password.setter
    def password(self, password_to_hash):
        self.password_hash = generate_password_hash(password_to_hash)

    def verify_password(self, password_to_compare):
        return check_password_hash(self.password_hash, password_to_compare)
