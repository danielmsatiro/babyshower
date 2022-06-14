from copy import deepcopy
from dataclasses import asdict
from http import HTTPStatus
from zoneinfo import available_timezones

from app.configs.database import db
from app.exceptions import InvalidKeyError, InvalidTypeValueError, NotAuthorizedError
from app.exceptions.parents_exc import (
    InvalidCpfLenghtError,
    InvalidEmailError,
    InvalidPhoneFormatError,
    NonexistentParentError,
    NotIsLoggedParentError,
)
from app.models import ParentModel
from app.models.cities_model import CityModel
from app.services.email_service import email_to_new_user
from flask import jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Query, Session


def pick_parents():
    params = request.args
    page = int(params.get("page", 1)) - 1
    per_page = int(params.get("per_page", 8))
    parent_id = params.get("parent_id", None)

    query: Query = db.session.query(
        ParentModel.id, ParentModel.username, ParentModel.name, ParentModel.image
    )

    if parent_id:
        response = query.filter_by(id=int(parent_id)).first()
        if not response:
            return {"msg": "No data found"}
        return {"user": response._asdict()}, HTTPStatus.OK

    query = query.offset(page * per_page).limit(per_page).all()
    response = [response._asdict() for response in query]
    if response == []:
        return {"msg": "No data found"}

    return {"users": response}, HTTPStatus.OK


@jwt_required()
def pick_parents_by_id(parent_id: int):
    user_logged = get_jwt_identity()

    try:

        parent: Query = ParentModel.query.get(parent_id)

        if not parent:
            raise NonexistentParentError

        if not parent_id == user_logged["id"]:
            raise NotIsLoggedParentError

        city: Query = CityModel.query.get(parent.city_point_id)

        new_parent = asdict(parent)

        new_parent["products"] = f"api/products/by_parent/{parent_id}"
        new_parent["city"] = city.city
        new_parent["state"] = city.state

        return jsonify(new_parent), HTTPStatus.OK

    except NonexistentParentError as err:
        return err.message, HTTPStatus.NOT_FOUND
    except NotIsLoggedParentError as e:
        return e.message, e.status


def new_parents():
    session: Session = db.session
    data: dict = request.get_json()
    user_current = data.copy()

    city = data["city"]
    state = data["state"]

    cities_query: Query = session.query(CityModel)

    point_id_current = (
        cities_query.filter(CityModel.state.ilike(f"%{data['state']}%"))
        .filter(CityModel.city.ilike(f"%{data['city']}%"))
        .first()
        .point_id
    )

    data.update({"city_point_id": point_id_current})

    data.pop("city")
    data.pop("state")

    received_key = set(user_current.keys())
    available_keys = {
        "cpf",
        "username",
        "name",
        "email",
        "password",
        "phone",
        "city",
        "state",
    }

    try:
        if not received_key == available_keys:
            raise InvalidKeyError(received_key, available_keys)

        # Valida o tipo dos dados passados

        for value in list(user_current):
            if type(user_current[value]) != str:
                raise InvalidTypeValueError

        parent = ParentModel(**data)

        session: Session = db.session
        session.add(parent)
        session.commit()

        city_state = (
            session.query(CityModel.city, CityModel.uf)
            .filter_by(point_id=point_id_current)
            .first()
        )

        city_state = {"city/state": f"{city_state[0]}/{city_state[1]}"}
        user_current.pop("city")
        user_current.pop("state")
        user_current.update(city_state)

    except (
        InvalidKeyError,
        InvalidTypeValueError,
        InvalidPhoneFormatError,
        InvalidCpfLenghtError,
        InvalidEmailError,
    ) as e:
        return e.message, e.status

    except IntegrityError as e:
        if type(e.orig) == UniqueViolation:
            return {
                "error": f"""{e.args[0].split(" ")[-4:-2]} already exists"""
            }, HTTPStatus.CONFLICT

    # email_to_new_user(parent.username, parent.email)

    return jsonify(user_current), HTTPStatus.CREATED


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

    return {"access_token": token, "id": found_parent.id}, HTTPStatus.OK


@jwt_required()
def update_parents():

    data: dict = request.get_json()

    user_logged = get_jwt_identity()

    received_key = set(data.keys())
    available_keys = {
        "username",
        "cpf",
        "name",
        "email",
        "password",
        "phone",
        "city",
        "state",
        "image",
    }

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

    except (InvalidKeyError, InvalidTypeValueError, InvalidPhoneFormatError) as e:
        return e.message, e.status

    city: Query = CityModel.query.get(parent.city_point_id)

    updated_parent = asdict(parent)

    updated_parent["products"] = f"api/products/by_parent/{updated_parent['id']}"
    updated_parent["city"] = city.city
    updated_parent["state"] = city.state

    return jsonify(updated_parent)


@jwt_required()
def delete_parents():
    user_logged = get_jwt_identity()
    session: Session = db.session
    base_query: Query = session.query(ParentModel)

    parent = base_query.filter_by(id=user_logged["id"]).first()

    session.delete(parent)
    session.commit()

    return "", HTTPStatus.NO_CONTENT
