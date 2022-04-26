from dataclasses import dataclass

from app.configs.database import db
from sqlalchemy import VARCHAR, Boolean, Column, ForeignKey, Integer, Numeric
from sqlalchemy.orm import relationship, backref


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
    title = Column(VARCHAR(128), nullable=False)
    price = Column(Numeric, nullable=False)
    parent_id = Column(Integer, nullable=False)
    description = Column(VARCHAR)
    image = Column(VARCHAR)
    sold = Column(Boolean, default=False)

    # AGUARDANDO EXISTENCIA DAS TABELAS DE REFERENCIA ABAIXO
    # parent_id = Column(Integer, ForeignKey('parents.id'), nullable=False)
    # categories = relationship(
    #     'Category',
    #     secondary='categories_products',
    #     backref=backref('products')
    # )

    questions = relationship(
        'QuestionModel', 
        backref="product", 
        uselist=True
    )