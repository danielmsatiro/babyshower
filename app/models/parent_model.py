import re
from dataclasses import dataclass

from app.configs.database import db
from app.exceptions import InvalidTypeValueError
from app.exceptions.parents_exc import (
    InvalidCpfLenghtError,
    InvalidEmailError,
    InvalidPhoneFormatError,
)
from app.models.cities_model import CityModel
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import backref, relationship, validates
from werkzeug.security import check_password_hash, generate_password_hash


@dataclass
class ParentModel(db.Model):

    __tablename__ = "parents"

    id: str = Column(Integer, primary_key=True, nullable=False)
    cpf: str = Column(String, nullable=False, unique=True)
    username: str = Column(String, nullable=False, unique=True)
    name: str = Column(String, nullable=False)
    email: str = Column(String, nullable=False, unique=True)
    password_hash = Column(String, nullable=False)
    phone: str = Column(String, nullable=False)
    image: str = Column(String)
    image_key: str = Column(String)

    city_point_id = Column(
        Integer, ForeignKey("cities.point_id", ondelete="CASCADE"), nullable=False
    )

    products = relationship("ProductModel", backref=backref("parent", uselist=False))

    questions = relationship("QuestionModel", backref=backref("parent", uselist=False))

    @property
    def password(self):
        raise AttributeError("Password cannot be accessed")

    @password.setter
    def password(self, password_to_hash):
        self.password_hash = generate_password_hash(password_to_hash)

    def verify_password(self, password_to_compare):
        return check_password_hash(self.password_hash, password_to_compare)

    @validates("cpf")
    def validate_cpf_type(self, key, cpf_to_be_tested):
        if type(cpf_to_be_tested) != str:
            raise InvalidTypeValueError(cpf_to_be_tested)

        if len(cpf_to_be_tested) != 11:
            raise InvalidCpfLenghtError

        return cpf_to_be_tested

    @validates("email")
    def validate_email(self, key, email):
        if not re.search(r"[\w\-.]+@[\w\-]+\.\w+\.?\w*", email):
            raise InvalidEmailError

        expected_providers = {
            "mail.com",
            "mail.com.br",
            "mail.org.br",
            "gmail.com",
            "gmail.com.br",
            "gmail.org.br",
            "hotmail.com",
            "hotmail.com.br",
            "hotmail.org.br",
            "kenzie.com",
            "kenzie.com.br",
            "kenzie.org.br",
            "outlook.com",
            "outlook.com.br",
            "outlook.org.br",
            "live.com",
            "live.com.br",
            "live.org.br",
            "yahoo.com",
            "yahoo.com.br",
            "yahoo.org.br",
        }

        received_provider = {email.split("@")[1]}

        if received_provider - expected_providers:
            raise InvalidEmailError

        return email.lower()

    @validates("phone")
    def validate_phone_type(self, key, phone_to_be_tested):
        valid = re.compile(
            r"^\((?:[14689][1-9]|2[12478]|3[1234578]|5[1345]|7[134579])\) (?:[2-8]|9[1-9])[0-9]{3}\-[0-9]{4}$"
        )
        if not valid.search(phone_to_be_tested):
            raise InvalidPhoneFormatError

        return phone_to_be_tested

    @validates("username", "name")
    def normalization(self, key, value):
        if key == "username":
            return value.lower()
        return value.title()
