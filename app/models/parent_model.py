from dataclasses import dataclass
import re

from app.exceptions.parents_exc import InvalidEmailLenghtError
from app.exceptions.parents_exc import InvalidTypeValueError
from app.exceptions.parents_exc import InvalidPhoneFormatError

from app.configs.database import db
from sqlalchemy.orm import backref, relationship
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import backref, relationship, validates
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

    products = relationship("ProductModel", backref=backref(
        "parent", uselist=False))

    questions = relationship("QuestionModel", backref=backref(
        "parent", uselist=False))

    @property
    def password(self):
        raise AttributeError("Password cannot be accessed")

    @password.setter
    def password(self, password_to_hash):
        self.password_hash = generate_password_hash(password_to_hash)

    def verify_password(self, password_to_compare):
        return check_password_hash(
            self.password_hash, password_to_compare)

    @validates("cpf")
    def validate_cpf_type(self, key, cpf_to_be_tested):
        if type(cpf_to_be_tested) != str:
            raise InvalidTypeValueError

        if len(cpf_to_be_tested) != 11:
            raise InvalidEmailLenghtError

        return cpf_to_be_tested

    @validates("email")
    def validate_email_type(self, key, email_to_be_tested):
        if type(email_to_be_tested) != str:
            raise InvalidTypeValueError

        return email_to_be_tested

    @validates("phone")
    def validate_phone_type(self, key, phone_to_be_tested):
        valid = re.compile(r"^\(\d{2}\)\s\d{4,5}\-\d{4}")
        if not valid.search(phone_to_be_tested):
            raise InvalidPhoneFormatError

        return phone_to_be_tested
