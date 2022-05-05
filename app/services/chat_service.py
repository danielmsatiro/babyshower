from dataclasses import asdict
from app.models import MessageModel, ParentModel
from app.configs.database import db
from flask import url_for
from sqlalchemy.orm import Session


def message_serialize(message: MessageModel, user_logged_id: int, other_parent_id: int) -> dict:
    session: Session = db.session
    if user_logged_id == other_parent_id or other_parent_id == message.parent_id:
        message.msg_read = True
        session.add(message)
        session.commit()

    serialize_message = asdict(message)

    find_parent: ParentModel = session.query(ParentModel).filter_by(
        id=message.parent_id
    ).first()
    
    serialize_message['parent'] = find_parent.username

    return serialize_message

def serialize_chat(chat):
    
    session: Session = db.session
    messages: MessageModel = session.query(MessageModel).filter_by(
        chat_id=chat['id']
    ).all()

    is_not_read = False

    for msg in messages:
        print(msg.msg_read)
        if msg.msg_read == False:
            is_not_read = True


    new_keys = {
        "link": url_for(
            "bp_api.bp_chat.read_chat",
            other_parent_id=chat['parent_id_retrieve'],
            ),
        "not_read": is_not_read
    }
    
    chat.update(new_keys)

    return chat