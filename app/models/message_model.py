from dataclasses import dataclass
import datetime
from email.policy import default

from app.configs.database import db
from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text


@dataclass
class MessageModel(db.Model):
    __tablename__ = "messages"

    now = datetime.datetime.utcnow()

    id = Column(Integer, primary_key=True)
    data = Column(DateTime, nullable=False, default=now)
    message = Column(Text, nullable=False)

    chat_id = Column(
        Integer, ForeignKey("chat.id", ondelete="CASCADE"), nullable=False
    )
