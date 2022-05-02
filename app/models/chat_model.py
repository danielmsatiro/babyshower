from dataclasses import dataclass
from datetime import datetime

from app.configs.database import db
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String


@dataclass
class ChatModel(db.Model):
    id: int
    data: datetime
    message: str
    confirmed_read: bool
    reader_id: int
    writer_id: int

    __tablename__ = "chat"
    id = Column(Integer, primary_key=True)
    data = Column(DateTime, nullable=False)
    message = Column(String, nullable=False)
    confirmed_read = Column(Boolean, default=False)
    reader_id = Column(
        Integer, ForeignKey("parents.id", ondelete="CASCADE"), nullable=False
    )
    writer_id = Column(
        Integer, ForeignKey("parents.id", ondelete="CASCADE"), nullable=False
    )
