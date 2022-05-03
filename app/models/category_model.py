from dataclasses import dataclass

from app.configs.database import db
from sqlalchemy import Column, Integer, String, Text


@dataclass
class CategoryModel(db.Model):

    __tablename__ = "categories"

    id: int
    name: str
    description: str

    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    description = Column(Text, default="")
