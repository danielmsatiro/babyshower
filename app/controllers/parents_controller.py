from http import HTTPStatus

from app.configs.database import db
from app.exceptions import InvalidKeyError, InvalidTypeValueError, NotAuthorizedError
from app.exceptions.parents_exc import InvalidCpfLenghtError, InvalidPhoneFormatError
from app.models import ParentModel
from app.services.email_service import email_to_new_user
from flask import jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Query, Session


def pick_parents():

    query: Query = db.session.query(ParentModel.id, ParentModel.username)

    response = query.all()

    response = [response._asdict() for response in query]

    if response == []:
        return {"msg": "No data found"}

    return {"users": response}, HTTPStatus.OK


def new_parents():

    data: dict = request.get_json()

    received_key = set(data.keys())
    available_keys = {"cpf", "username", "name", "email", "password", "phone"}

    try:
        if not received_key == available_keys:
            raise InvalidKeyError(received_key, available_keys)

        for key, value in data.items():
            if type(value) != str:
                raise InvalidTypeValueError(key)

        parent = ParentModel(**data)

        session: Session = db.session
        session.add(parent)
        session.commit()

    except InvalidKeyError as e:
        return e.message, e.status

    except InvalidTypeValueError as e:
        return e.message, e.status

    except InvalidCpfLenghtError as e:
        return e.message, e.status

    except InvalidPhoneFormatError as e:
        return e.message, e.status

    except IntegrityError as e:
        if type(e.orig) == UniqueViolation:
            return {
                "error": f"""{e.args[0].split(" ")[-4:-2]} already exists"""
            }, HTTPStatus.CONFLICT

    email_to_new_user(parent.username, parent.email)

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

    try:
        if not found_parent.verify_password(parent_data["password"]):
            raise NotAuthorizedError

    except NotAuthorizedError as e:
        return e.message, e.status

    information_for_encoding = {
        "id": found_parent.id,
        "username": found_parent.username,
    }

    token = create_access_token(information_for_encoding)

    return {"access_token": token}, HTTPStatus.OK


@jwt_required()
def update_parents():

    data: dict = request.get_json()

    user_logged = get_jwt_identity()

    received_key = set(data.keys())
    available_keys = {"username", "name", "email", "password", "phone"}

    try:
        if received_key - available_keys:
            raise InvalidKeyError(received_key, available_keys)

        for key, value in data.items():
            if type(value) != str:
                raise InvalidTypeValueError(key)

        session: Session = db.session

        parent: Query = session.query(ParentModel)
        parent = parent.filter_by(id=user_logged["id"]).first()

        for key, value in data.items():
            setattr(parent, key, value)

            session.add(parent)
            session.commit()

    except InvalidKeyError as e:
        return e.message, e.status
    except InvalidTypeValueError as e:
        return e.message, e.status
    except InvalidPhoneFormatError as e:
        return e.message, e.status

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
