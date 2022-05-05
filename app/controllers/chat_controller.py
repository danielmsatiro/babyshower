import datetime
from dataclasses import asdict
from flask import jsonify, request
from sqlalchemy.orm import Query, Session
from app.configs.database import db
from app.models.chat_model import ChatModel
from app.models.parent_model import ParentModel
from app.models.message_model import MessageModel
from flask_jwt_extended import get_jwt_identity, jwt_required
from ipdb import set_trace


@jwt_required()
def read_chat(other_parent_id):
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

    messages: MessageModel = session.query(MessageModel).filter_by(
        chat_id=chat_refer.id
    )

    page = int(params.get("page", 1)) - 1
    per_page = int(params.get("per_page", 10))
    messages: Query = messages.offset(page * per_page).limit(per_page).all()

    # últimas 10 mensagens -> pode aumentar
    # alterar para lido -> segue a lógica de um update
    # alterar model com data de lido
    ...
    messages_serialize = [ asdict(msg) for msg in messages]
    
    return {"messages": messages_serialize}, 200


@jwt_required()
def post_message(other_parent_id: int):

    user_logged = get_jwt_identity()

    session: Session = db.session
    data = request.get_json()

    parents_query = session.query(ParentModel)
    chat_query = session.query(ChatModel)

    chat_refer: ChatModel = chat_query.filter_by(
        parent_id_main=user_logged["id"]).filter_by(
        parent_id_retrieve=int(other_parent_id)
    ).first()
    if not chat_refer:
        chat_refer: ChatModel = chat_query.filter_by(
            parent_id_retrieve=user_logged["id"]).filter_by(
            parent_id_main=int(other_parent_id)
        ).first()

    user_refer = parents_query.filter_by(id=int(other_parent_id)).first()

    if user_refer and not chat_refer:
        user_logged_id = user_logged["id"]
        chat_refer: ChatModel = ChatModel(
            parent_id_main=user_logged_id,
            parent_id_retrieve=other_parent_id)

    now = datetime.datetime.utcnow().strftime('%d/%m/%Y')

    chat_refer.last_data_update = now

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

    return jsonify("Mensagem enviada com sucesso!"), 200
