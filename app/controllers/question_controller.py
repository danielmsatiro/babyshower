from datetime import datetime as dt
from http import HTTPStatus
from sqlalchemy import exc

from sqlalchemy.sql.traversals import COMPARE_SUCCEEDED

from app.configs.database import db
from app.exceptions import (
    InvalidKeyError,
    InvalidTypeValueError,
    NotAuthorizedError,
    NotFoundError,
)
from app.models import QuestionModel
from app.models.parent_model import ParentModel
from app.models.product_model import ProductModel
from app.services.email_service import email_new_question
from app.services.question_service import serialize_answer
from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy.orm import Query, Session


def get_product_questions(product_id: int):
    params = request.args
    page = int(params.get("page", 1)) - 1
    per_page = int(params.get("per_page", 8))

    base_query: Query = db.session.query(QuestionModel)

    questions = (
        base_query.filter(QuestionModel.product_id == product_id)
        .offset(page * per_page)
        .limit(per_page)
        .all()
    )

    serialized_questions = [serialize_answer(question) for question in questions]

    return jsonify(serialized_questions), HTTPStatus.OK


@jwt_required()
def create_question(product_id: int):
    data: dict = request.get_json()

    user_logged = get_jwt_identity()

    data["created_at"] = dt.now()
    data["parent_id"] = user_logged["id"]
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

        lead: ParentModel = (
            session.query(ParentModel).filter_by(id=question.parent_id).first()
        )
        owner: ParentModel = (
            session.query(ParentModel).filter_by(id=product.parent_id).first()
        )
        email_new_question(
            owner.username, product.title, owner.email, lead.username, question.question
        )

        return jsonify(question), HTTPStatus.CREATED

    except NotFoundError as e:
        return e.message, e.status


@jwt_required()
def update_question(question_id: int):
    data: dict = request.get_json()
    received_key = set(data.keys())
    expected_key = {"question"}
    user_logged = get_jwt_identity()

    session: Session = db.session
    
    try:
        if not received_key == expected_key:
            raise InvalidKeyError(received_key, expected_key)
        
        if not type(data.get("question")) == str:
            raise InvalidTypeValueError
        
        
        
        question = session.query(QuestionModel).get(question_id)

        if not question:
            raise NotFoundError(question_id, "question")

        if user_logged["id"] == question.parent_id:
            data["updated_at"] = dt.now()
            for key, value in data.items():
                setattr(question, key, value)
            session.commit()
        else:
            raise NotAuthorizedError

        return jsonify(question), HTTPStatus.OK

    except NotFoundError as e:
        return e.message, e.status
    except NotAuthorizedError as e:
        return e.message, e.status
    except InvalidKeyError as e:
        return e.message, e.status
    except InvalidTypeValueError as e:
        return e.message, e.status
     



@jwt_required()
def delete_question(question_id: int):
    session: Session = db.session

    user_logged = get_jwt_identity()

    question = session.query(QuestionModel).filter_by(id=question_id).first()

    try:
        if not question:
            raise NotFoundError(question_id, "question")

        if user_logged["id"] == question.parent_id:
            session.delete(question)
            session.commit()

        else:
            raise NotAuthorizedError

        return "", HTTPStatus.NO_CONTENT

    except NotFoundError as e:
        return e.message, e.status
    except NotAuthorizedError as e:
        return e.message, e.status
