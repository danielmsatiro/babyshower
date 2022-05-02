from dataclasses import dataclass

from app.configs.database import db
from app.exceptions import InvalidTypeValueError
from app.exceptions.products_exceptions import InvalidTypeNumberError
from sqlalchemy import Boolean, Column, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import backref, relationship, validates


@dataclass
class ProductModel(db.Model):
    __tablename__ = "products"

    id: int
    title: str
    price: float
    parent_id: int
    description: str
    image: str
    sold: bool
    categories: list

    id = Column(Integer, primary_key=True)
    title = Column(String(128), nullable=False)
    price = Column(Numeric, nullable=False)
    parent_id = Column(
        Integer, ForeignKey("parents.id", ondelete="CASCADE"), nullable=False
    )
    description = Column(String)
    image = Column(String)
    sold = Column(Boolean, default=False)

    categories = relationship(
        "CategoryModel", secondary="product_category", backref=backref("products")
    )

    @validates("title", "price", "parent_id", "description", "image")
    def validates_product_values(self, key, value):

        str_values = ["title", "description", "image"]

        if key in str_values:

            if type(value) != str:
                raise InvalidTypeValueError(key)

        if key == "price":

            if type(value) != float:
                raise InvalidTypeNumberError(key)

        return value

    # questions = relationship(
    #     'QuestionModel',
    #     backref=backref('product', uselist=True)
    # )
