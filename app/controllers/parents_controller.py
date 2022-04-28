from http import HTTPStatus
from app.configs.database import db
from app.models import ParentModel
from flask import jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from sqlalchemy.orm import Query, Session


def pick_parents():

    query: Query = db.session.query(ParentModel.id, ParentModel.username)

    response = query.all()

    response = [response._asdict() for response in query]

    return {"users": response}, HTTPStatus.OK


def new_parents():

    data: dict = request.get_json()

    parent = ParentModel(**data)

    session: Session = db.session

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

    token = create_access_token(found_parent)

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

    return jsonify(parent.username)


@jwt_required()
def delete_parents():
    user_logged = get_jwt_identity()
    session: Session = db.session
    base_query: Query = session.query(ParentModel)

    parent = base_query.filter_by(id=user_logged["id"]).first()

    session.delete(parent)
    session.commit()

    return "", HTTPStatus.NO_CONTENT
