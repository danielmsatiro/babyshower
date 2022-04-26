from sqlalchemy import Column, ForeignKey, Integer, Text
from dataclasses import dataclass
from app.configs.database import db


@dataclass
class Categories(db.Model):

    __tablename__ = "Categories"

    id = Column(Integer, primary_key=True)
    description = Column(Text, default="")
