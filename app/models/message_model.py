from dataclasses import dataclass
import datetime

from app.configs.database import db
from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text


@dataclass
class MessageModel(db.Model):
    __tablename__ = "messages"
    now = datetime.datetime.utcnow()

    data: DateTime
    message: str

    id = Column(Integer, primary_key=True)
    data = Column(DateTime, nullable=False, default=now)
    message = Column(Text, nullable=False)

    chat_id = Column(
        Integer, ForeignKey("chat.id", ondelete="CASCADE"), nullable=False
    )
