from http import HTTPStatus
from zoneinfo import available_timezones

from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation
from app.exceptions.parents_exc import InvalidTypeValueError, InvalidEmailLenghtError, InvalidPhoneFormatError

from app.configs.database import db
from app.models import ParentModel
from flask import jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
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

    wrong_keys = []
    available_keys = ["cpf", "username", "name", "email", "password", "phone"]
    for key in data.keys():
        if key not in available_keys:
            wrong_keys.append(key)
    
    #Valida o tipo dos dados passados
    for value in list(data):
        if type(data[value]) != str:
            return {"error": f"The value of {value} must be a string"}, HTTPStatus.BAD_REQUEST

    try:
        parent = ParentModel(**data)
    except TypeError as e:
        return {
            "available_keys": f"{available_keys}",
            "wrong_keys": f"{wrong_keys}"
        }, HTTPStatus.BAD_REQUEST
    except InvalidEmailLenghtError as e:
        return e.message, e.status
    except InvalidPhoneFormatError as e:
        return e.message, e.status

    try:
        session: Session = db.session
        session.add(parent)
        session.commit()
    except IntegrityError as e:
        if type(e.orig) == UniqueViolation:
            print(e.args)
            return {"error": f"""{e.args[0].split(" ")[-4:-2]} already exists"""}, HTTPStatus.CONFLICT

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

    data: dict = request.get_json()

    wrong_keys = []
    available_keys = ["cpf", "username", "name", "email", "password", "phone"]
    for key in data.keys():
        if key not in available_keys:
            wrong_keys.append(key)
    
    #Valida as chaves passadas
    if len(wrong_keys) != 0:
        return {
            "available_keys": f"{available_keys}",
            "wrong_keys": f"{wrong_keys}"
        }, HTTPStatus.BAD_REQUEST
             

    user_logged = get_jwt_identity()

    #Valida o tipo dos dados
    for value in list(data):
        if type(data[value]) != str:
            return {"error": f"The value of {value} must be a string"}, HTTPStatus.BAD_REQUEST

    session: Session = db.session

    parent: Query = session.query(ParentModel)
    parent = parent.filter_by(id=user_logged["id"]).first()

    for key, value in data.items():
        setattr(parent, key, value)
    
    try:
        session.add(parent)
        session.commit()

    #Valida o formato de telefone
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
