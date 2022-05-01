from http import HTTPStatus
from app.configs.database import db
from app.models import ParentModel
from flask import jsonify, request
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy.orm import Query, Session


def pick_parents():

    query: Query = db.session.query(
        ParentModel.id, ParentModel.username, ParentModel.name,
        ParentModel.estado, ParentModel.nome_municipio
    )

    response = query.all()

    response = [response._asdict() for response in query]

    return {"users": response}, HTTPStatus.OK


def new_parents():

    session: Session = db.session
    data: dict = request.get_json()

    parent = ParentModel(**data)

    session.add(parent)

    session.commit()

    return jsonify(parent), HTTPStatus.CREATED


def login():
    parent_data = request.get_json()

    found_parent: ParentModel = ParentModel.query.filter(
        (ParentModel.cpf == parent_data.get("cpf"))
        | (ParentModel.email == parent_data.get("email"))
        | (ParentModel.username == parent_data.get("username"))
    ).first()

    if not found_parent:
        return {"message": "User not found"}, HTTPStatus.NOT_FOUND

    if not found_parent.verify_password(parent_data["password"]):
        return {"message": "Unauthorized"}, HTTPStatus.UNAUTHORIZED

    information_for_encoding = {
        "id": found_parent.id,
        "username": found_parent.username,
    }

    token = create_access_token(information_for_encoding)

    return {"access_token": token}, HTTPStatus.OK


@jwt_required()
def update_parents():

    user_logged = get_jwt_identity()

    data: dict = request.get_json()

    session: Session = db.session

    parent: Query = session.query(ParentModel)
    parent = parent.filter_by(id=user_logged["id"]).first()

    for key, value in data.items():
        setattr(parent, key, value)

    session.add(parent)

    session.commit()

    return jsonify(parent)


@jwt_required()
def delete_parents():
    user_logged = get_jwt_identity()
    session: Session = db.session
    base_query: Query = session.query(ParentModel)

    parent = base_query.filter_by(id=user_logged["id"]).first()

    session.delete(parent)
    session.commit()

    return "", HTTPStatus.NO_CONTENT
