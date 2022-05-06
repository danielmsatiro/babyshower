from bdb import set_trace
from datetime import datetime as dt
from http import HTTPStatus
from flask import jsonify, request
from sqlalchemy.orm import Query, Session
from app.configs.database import db
from app.exceptions import InvalidKeyError, InvalidTypeValueError, NotFoundError
from app.exceptions.chat_exception import UserOrChatNotFoundError
from app.models.chat_model import ChatModel
from app.models.parent_model import ParentModel
from app.models.message_model import MessageModel
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy import desc
from dataclasses import asdict
from ipdb import set_trace

from app.services.chat_service import message_serialize, serialize_chat


@jwt_required()
def read_chat(other_parent_id):
    try:
        user_logged = get_jwt_identity()
        params = dict(request.args.to_dict().items())

        session: Session = db.session
        chat_refer: ChatModel = session.query(ChatModel).filter_by(
            parent_id_main=user_logged["id"]).filter_by(
            parent_id_retrieve=other_parent_id
        ).first()
        if not chat_refer:
            chat_refer: ChatModel = session.query(ChatModel).filter_by(
                parent_id_retrieve=user_logged["id"]).filter_by(
                parent_id_main=int(other_parent_id)
            ).first()
        print(chat_refer)

        if not chat_refer:
            raise UserOrChatNotFoundError

        messages: MessageModel = session.query(MessageModel).filter_by(
            chat_id=chat_refer.id
        ).order_by(desc(MessageModel.data))

        page = int(params.get("page", 1)) - 1
        per_page = int(params.get("per_page", 10))
        messages: Query = messages.offset(page * per_page).limit(per_page).all()

        messages_serialize = [ message_serialize(msg, user_logged["id"], other_parent_id) for msg in messages ]
        
        return {"messages": messages_serialize}, 200

    except UserOrChatNotFoundError as e:
        return e.message, e.status
    


@jwt_required()
def post_message(other_parent_id: int):

    data: dict = request.get_json()
    received_keys = set(data.keys())
    expected_key = {'message'}

    try:
        if not received_keys == expected_key:
            raise InvalidKeyError(received_keys, expected_key)
        
        for key, value in data.items():
            if not type(value) == str:
                raise InvalidTypeValueError(key)

        user_logged = get_jwt_identity()

        session: Session = db.session

        parents_query = session.query(ParentModel)
        chat_query = session.query(ChatModel)

        user_refer = parents_query.filter_by(id=other_parent_id).first()
        if not user_refer:
            raise NotFoundError(other_parent_id, "parent")

        chat_refer: ChatModel = chat_query.filter_by(
            parent_id_main=user_logged["id"]).filter_by(
            parent_id_retrieve=int(other_parent_id)
        ).first()
        
        if not chat_refer:
            chat_refer: ChatModel = chat_query.filter_by(
                parent_id_retrieve=user_logged["id"]).filter_by(
                parent_id_main=int(other_parent_id)
            ).first()

        if not chat_refer:
            user_logged_id = user_logged["id"]
            chat_refer: ChatModel = ChatModel(
                parent_id_main=user_logged_id,
                parent_id_retrieve=other_parent_id)

        session.add(chat_refer)
        session.commit()

        message_current = MessageModel(
            message=data["message"],
            data=dt.now(),
            chat_id=chat_refer.id,
            parent_id=user_logged["id"]
        )

        session.add(message_current)
        session.commit()

        return jsonify({"msg": "Mensagem enviada com sucesso!"}), HTTPStatus.CREATED
    
    except InvalidKeyError as e:
        return e.message, e.status
    except InvalidTypeValueError as e:
        return e.message, e.status
    except NotFoundError as e:
        return e.message, e.status


@jwt_required()
def chats_by_parent():
    user_logged = get_jwt_identity()

    session: Session = db.session

    try:
        # Pegar chat de user_onwer para user_onwer
        chat_refer_id_main = session.query(ChatModel).filter_by(
                parent_id_main=user_logged["id"]
        )

        chat_refer_id_main = [chat.id for chat in chat_refer_id_main]

        # Pegar chat de user_onwer para other_user
        chat_refer_id_retrieve = session.query(ChatModel).filter_by(
                parent_id_retrieve=user_logged["id"]
        )

        chat_refer_id_retrieve = [chat.id for chat in chat_refer_id_retrieve]

        chat_refer_id_main.append(chat_refer_id_retrieve[0])

        chat_refer_ids = set(chat_refer_id_main)
        chat_refer_ids = list(chat_refer_ids)

        chat_user = session.query(ChatModel).filter(
                ChatModel.id.in_(chat_refer_ids)
        ).all()

        serialize_chats = []

        for chat in chat_user:
            chat: ChatModel
            new_messages = session.query(ChatModel).filter_by(
                    parent_id_main=chat.parent_id_main
                ).filter_by(
                    parent_id_retrieve=chat.parent_id_retrieve
                ).all()[0].id
            new_messages = session.query(MessageModel).filter_by(
                chat_id=new_messages
            )
            if new_messages:
                chat = {
                    "other_parent_id": chat.parent_id_retrieve,
                    "messages": f"chat/{chat.parent_id_retrieve}",
                    "read": new_messages.all()[-1].msg_read
                }
                serialize_chats.append(chat)
    except IndexError:
        return {
            "details": "You do not have chat initialized"
        }, HTTPStatus.NOT_FOUND

    return {"chats": serialize_chats}, 200
