from dataclasses import dataclass

from app.configs.database import db
from sqlalchemy import (
    String, 
    Boolean, 
    Column, 
    ForeignKey, 
    Integer, 
    Numeric
)
from sqlalchemy.orm import relationship, backref, validates

# Exceptions Importations
from app.exceptions.products_exceptions import (
    InvalidDataError
)


@dataclass
class ProductModel(db.Model):
    __tablename__ = 'products'

    id: int
    title: str
    price: float
    parent_id: int
    description: str
    image: str
    sold: bool

    id = Column(Integer, primary_key=True)
    title = Column(String(128), nullable=False)
    price = Column(Numeric, nullable=False)
    parent_id = Column(Integer, ForeignKey('parents.id'), nullable=False)
    description = Column(String)
    image = Column(String)
    sold = Column(Boolean, default=False)

    categories = relationship(
        'CategoryModel',
        secondary='product_category',
        backref=backref('products')
    )

    questions = relationship(
        'QuestionModel', 
        backref=backref('product', uselist=True)
    )

    @validates(
        "title",
        "price",
        "description",
        "image"
    )
    def validates_product_values(
        self, 
        key,
        value
    ):

        str_values = [
            "title",
            "description",
            "image"
        ]

        if key in str_values:
            
            if type(value) != str:
                raise InvalidDataError(
                    description={
                        "error": f"The value of keys: {str_values} needs to be String!"
                    } 
                )

        if key == "price":

            if type(value) != float:
                raise InvalidDataError(
                    description={
                        "error": f"The value of key: 'price' needs to be Float!"
                    }
                )

        return value
