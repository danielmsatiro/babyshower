from bdb import set_trace
from http import HTTPStatus

from sqlalchemy.exc import IntegrityError

from app.configs.database import db
from app.models import QuestionModel
from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.orm import Query, Session
from ipdb import set_trace


def get_product_questions(product_id: int):

    base_query: Query = db.session.query(QuestionModel)

    questions = base_query.filter(QuestionModel.product_id == product_id).all()
    serialized_questions = [question.__dict__ for question in questions]

    [question.pop("_sa_instance_state") for question in serialized_questions]

    return jsonify(serialized_questions), HTTPStatus.OK


@jwt_required()
def create_question(product_id: int):
    data: dict = request.get_json()

    parent = get_jwt_identity()

    data["parent_id"] = parent["id"]

    data["product_id"] = product_id
    try:
        question = QuestionModel(**data)

        session: Session = db.session

        session.add(question)
        session.commit()
    except IntegrityError:
        return {"Error": "Product not found"}

    return jsonify(question), HTTPStatus.CREATED


@jwt_required()
def update_question(question_id: int):
    data: dict = request.get_json()

    parent = get_jwt_identity()

    session: Session = db.session

    question = session.query(QuestionModel).get(question_id)

    if parent["id"] == question.parent_id:
        for key, value in data.items():
            setattr(question, key, value)
        session.commit()
    else:
        return {"msg": "Unauthorized action"}, HTTPStatus.UNAUTHORIZED

    return jsonify(question), HTTPStatus.OK


@jwt_required()
def delete_question(question_id: int):
    session: Session = db.session

    parent = get_jwt_identity()

    question = session.query(QuestionModel).filter_by(id=question_id).first()

    if parent["id"] == question.parent_id:
        session.delete(question)

        session.commit()
    else:
        return {"msg": "Unauthorized action"}, HTTPStatus.UNAUTHORIZED

    return "", HTTPStatus.NO_CONTENT
