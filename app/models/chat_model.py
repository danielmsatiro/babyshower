from dataclasses import dataclass
import datetime
from email.policy import default

from app.configs.database import db
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String


@dataclass
class ChatModel(db.Model):
    __tablename__ = "chat"

    now = datetime.datetime.utcnow().strftime('%d/%m/%Y')

    id = Column(Integer, primary_key=True)
    data: str = Column(DateTime, nullable=False, default=now)
    last_data_update: str = Column(DateTime, nullable=False, default=now)

    parent_id_main: int = Column(
        Integer, ForeignKey("parents.id", ondelete="CASCADE"), nullable=False
    )

    parent_id_retrieve: int = Column(
        Integer, ForeignKey("parents.id", ondelete="CASCADE"), nullable=False
    )
