from dataclasses import dataclass
from datetime import datetime as dt
from app.configs.database import db
from sqlalchemy import Column, DateTime, ForeignKey, Integer


@dataclass
class ChatModel(db.Model):
    __tablename__ = "chat"

    now = dt

    id: int = Column(Integer, primary_key=True)
    data: str = Column(DateTime, nullable=False, default=now)
    last_data_update: str = Column(DateTime, nullable=False, default=now)

    parent_id_main: int = Column(
        Integer, ForeignKey("parents.id", ondelete="CASCADE"), nullable=False
    )

    parent_id_retrieve: int = Column(
        Integer, ForeignKey("parents.id", ondelete="CASCADE"), nullable=False
    )
