from copy import deepcopy
from http import HTTPStatus

from app.configs.database import db
from app.models import ParentModel, ProductModel
from flask import jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from sqlalchemy.orm import Query, Session
from sqlalchemy.util.langhelpers import constructor_copy


def pick_parents():
    idd = 3
    query_product_by_parent: Query = (
        db.session.query(ProductModel.id)
        .select_from(ParentModel)
        .join(ProductModel)
        .filter(ProductModel.parent_id != idd)
        .all()
    )
    ids_product_by_parent = [response._asdict()["id"] for response in query_product_by_parent]
    print(ids_product_by_parent)

    query: Query = db.session.query(ParentModel.username)
    response = query.all()

    response = [response._asdict()["username"] for response in query]

    return {"usernames": response}, HTTPStatus.OK


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
def update_parents(parent_cpf):

    compare_cpf = get_jwt_identity()

    data: dict = request.get_json()
    
    session: Session = db.session
    
    parent: Query = session.query(ParentModel)
    parent = parent.filter_by(cpf=parent_cpf).first()

    if(compare_cpf["cpf"] == parent_cpf):
        
        for key, value in data.items():
            setattr(parent, key, value)

        session.add(parent)

        session.commit()

        return jsonify(parent)
    else:
        return {"error": "invalid cpf"}

@jwt_required()
def delete_parents(parent_cpf):
    compare_cpf = get_jwt_identity()
    session: Session = db.session
    base_query: Query = session.query(ParentModel)

    parent = base_query.filter_by(cpf=parent_cpf).first()

    if(compare_cpf["cpf"] == parent_cpf):
        session.delete(parent)
        session.commit()
    else:
        return {"error": "invalid cpf"}

    return "", HTTPStatus.NO_CONTENT
