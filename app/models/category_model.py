from sqlalchemy import Column, Integer, Text, String
from dataclasses import dataclass
from app.configs.database import db


@dataclass
class CategoryModel(db.Model):

    __tablename__ = "categories"

    id: int
    name: str
    description: str

    id = Column(Integer, primary_key=True)
    name = Column(String(128), unique=True, nullable=False)
    description = Column(Text, default="")
