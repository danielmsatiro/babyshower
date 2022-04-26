from app.configs.database import db
from dataclasses import dataclass
from sqlalchemy import Column, Integer, ForeignKey


@dataclass
class CategoryProductModel(db.Model):

    __tablename__ = "category_product"

    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)
    categories_id = Column(
        Integer, ForeignKey("categories.id"), nullable=False)
