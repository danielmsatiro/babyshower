from bdb import set_trace
from http import HTTPStatus
from sqlalchemy import exc

from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql.traversals import COMPARE_SUCCEEDED

from app.configs.database import db
from app.exceptions.question_exc import NotAuthorizedError
from app.exceptions import InvalidKeyError, InvalidTypeValueError, NotFoundError
from app.models import QuestionModel
from app.models.product_model import ProductModel
from flask import jsonify, request, session
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.orm import Query, Session
from ipdb import set_trace

from app.services.question_service import serialize_answer


def get_product_questions(product_id: int):

    base_query: Query = db.session.query(QuestionModel)

    questions = base_query.filter(QuestionModel.product_id == product_id).all()

    serialized_questions = [serialize_answer(question) for question in questions]

    # [question.pop("_sa_instance_state") for question in serialized_questions]

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

        product: ProductModel = (
            session.query(ProductModel).filter_by(id=product_id).first()
        )
        if not product:
            raise NotFoundError(product_id, "product")
        session.add(question)
        session.commit()
    except NotFoundError as e:
        return e.message, e.status

    return jsonify(question), HTTPStatus.CREATED


@jwt_required()
def update_question(question_id: int):
    data: dict = request.get_json()
    received_key = set(data.keys())
    expected_key = {"question"}
    parent = get_jwt_identity()

    session: Session = db.session

    try:
        if not type(data["question"]) == str:
            raise InvalidTypeValueError

        if not received_key == expected_key:
            raise InvalidKeyError(received_key, expected_key)

        question = session.query(QuestionModel).get(question_id)

        if not question:
            raise NotFoundError(question_id, "question")

        if parent["id"] == question.parent_id:
            for key, value in data.items():
                setattr(question, key, value)
            session.commit()
        else:
            raise NotAuthorizedError

    except NotFoundError as e:
        return e.message, e.status
    except NotAuthorizedError as e:
        return e.message, e.status
    except InvalidKeyError as e:
        return e.message, e.status
    except InvalidTypeValueError as e:
        return e.message, e.status

    return jsonify(question), HTTPStatus.OK


@jwt_required()
def delete_question(question_id: int):
    session: Session = db.session

    parent = get_jwt_identity()

    question = session.query(QuestionModel).filter_by(id=question_id).first()

    try:
        if not question:
            raise NotFoundError(question_id, "question")

        if parent["id"] == question.parent_id:

            session.delete(question)

            session.commit()

        else:
            raise NotAuthorizedError

    except NotFoundError as e:
        return e.message, e.status
    except NotAuthorizedError as e:
        return e.message, e.status

    return "", HTTPStatus.NO_CONTENT
