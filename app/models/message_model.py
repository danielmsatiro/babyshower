from dataclasses import dataclass
import datetime

from app.configs.database import db
from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text, Boolean


@dataclass
class MessageModel(db.Model):
    __tablename__ = "messages"
    now = datetime.datetime.utcnow().strftime('%d/%m/%Y')

    data: DateTime
    message: str

    id = Column(Integer, primary_key=True)
    data = Column(DateTime, nullable=False, default=now)
    message = Column(Text, nullable=False)

    msg_read = Column(Boolean, nullable=False, default=False)

    parent_id = Column(
        Integer, ForeignKey("parents.id", ondelete="CASCADE"), nullable=False
    )

    chat_id = Column(
        Integer, ForeignKey("chat.id", ondelete="CASCADE"), nullable=False
    )
