from dataclasses import dataclass

from app.configs.database import db
from sqlalchemy import String, Boolean, Column, ForeignKey, Integer, Numeric
from sqlalchemy.orm import relationship, backref


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
    parent_id = Column(Integer, ForeignKey("parents.id"), nullable=False)
    description = Column(String)
    image = Column(String)
    sold = Column(Boolean, default=False)

    categories = relationship(
        "CategoryModel", secondary="product_category", backref=backref("products")
    )

    questions = relationship("QuestionModel", backref=backref("product", uselist=True))
