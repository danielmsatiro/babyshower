from dataclasses import asdict
from app.models import MessageModel, ParentModel
from app.configs.database import db
from sqlalchemy.orm import Session


def message_serialize(message: MessageModel, other_parent_id: int) -> dict:
    session: Session = db.session
    if other_parent_id == message.parent_id:
        message.msg_read = True
        session.add(message)
        session.commit()

    serialize_message = asdict(message)

    find_parent: ParentModel = session.query(ParentModel).filter_by(
        id=message.parent_id
    ).first()
    
    serialize_message['parent'] = find_parent.username

    return serialize_message