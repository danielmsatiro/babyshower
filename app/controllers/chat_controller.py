import datetime
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

from app.services.chat_service import message_serialize


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

        messages_serialize = [ message_serialize(msg, other_parent_id) for msg in messages ]
        
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
            data=datetime.datetime.utcnow(),
            chat_id=chat_refer.id,
            parent_id=user_logged["id"]
        )

        session.add(message_current)
        session.commit()

        return jsonify("Mensagem enviada com sucesso!"), HTTPStatus.OK
    
    except InvalidKeyError as e:
        return e.message, e.status
    except InvalidTypeValueError as e:
        return e.message, e.status
    except NotFoundError as e:
        return e.message, e.status
