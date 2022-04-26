from sqlalchemy import Column, Integer, Text
from dataclasses import dataclass
from app.configs.database import db


@dataclass
class CategoryModel(db.Model):

    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    description = Column(Text, default="")
