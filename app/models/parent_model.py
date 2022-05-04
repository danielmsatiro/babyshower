import re
from dataclasses import dataclass

from app.configs.database import db
from app.exceptions import InvalidTypeValueError
from app.exceptions.parents_exc import InvalidCpfLenghtError, InvalidPhoneFormatError
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import backref, relationship, validates
from werkzeug.security import check_password_hash, generate_password_hash
from app.models.cities_model import CityModel


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
    def validate_email_type(self, key, email_to_be_tested):
        if type(email_to_be_tested) != str:
            raise InvalidTypeValueError

        return email_to_be_tested

    @validates("phone")
    def validate_phone_type(self, key, phone_to_be_tested):
        valid = re.compile(
            r"^\((?:[14689][1-9]|2[12478]|3[1234578]|5[1345]|7[134579])\) (?:[2-8]|9[1-9])[0-9]{3}\-[0-9]{4}$"
        )
        if not valid.search(phone_to_be_tested):
            raise InvalidPhoneFormatError

        return phone_to_be_tested
