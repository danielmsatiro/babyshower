from datetime import datetime as dt
from http import HTTPStatus

from app.configs.database import db
from app.exceptions import (
    InvalidKeyError,
    InvalidTypeValueError,
    NotAuthorizedError,
    NotFoundError,
)
from app.models.answer_model import AnswerModel
from app.models.parent_model import ParentModel
from app.models.product_model import ProductModel
from app.models.question_model import QuestionModel
from app.services.answer_service import serialize_answer
from app.services.email_service import email_new_answer
from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy.orm import Session


@jwt_required()
def create_answer(question_id: int):
    data = request.get_json()
    user_logged = get_jwt_identity()

    received_key = set(data.keys())
    expected_key = {"answer"}

    session: Session = db.session

    try:
        if not type(data["answer"]) == str:
            raise InvalidTypeValueError

        if not received_key == expected_key:
            raise InvalidKeyError(received_key, expected_key)

        question: QuestionModel = (
            session.query(QuestionModel).filter_by(id=question_id).first()
        )
        if not question:
            raise NotFoundError(question_id, "Question")

        product: ProductModel = (
            session.query(ProductModel).filter_by(id=question.product_id).first()
        )

        if user_logged["id"] != product.parent_id:
            raise NotAuthorizedError

        data["created_at"] = dt.now()
        data["parent_id"] = user_logged["id"]
        data["question_id"] = question_id

        new_answer: AnswerModel = AnswerModel(**data)

        session.add(new_answer)
        session.commit()

        lead: ParentModel = (
            session.query(ParentModel).filter_by(id=question.parent_id).first()
        )
        owner: ParentModel = (
            session.query(ParentModel).filter_by(id=product.parent_id).first()
        )

        email_new_answer(
            lead.username, product.title, lead.email, owner.username, new_answer.answer
        )

        return jsonify(serialize_answer(new_answer)), HTTPStatus.CREATED

    except (
        NotFoundError,
        NotAuthorizedError,
        InvalidKeyError,
        InvalidTypeValueError,
    ) as e:
        return e.message, e.status


def read_answer(answer_id: int):
    try:
        answer = AnswerModel.query.filter_by(id=answer_id).first()
        if not answer:
            raise NotFoundError(answer_id, "answer")
        return jsonify(serialize_answer(answer)), HTTPStatus.OK
    except NotFoundError as e:
        return e.message, e.status


@jwt_required()
def update_answer(answer_id: int):
    data = request.get_json()
    user_logged = get_jwt_identity()

    received_key = set(data.keys())
    expected_key = {"answer"}

    session: Session = db.session

    try:
        if not type(data["answer"]) == str:
            raise InvalidTypeValueError

        if not received_key == expected_key:
            raise InvalidKeyError(received_key, expected_key)

        answer: AnswerModel = session.query(AnswerModel).filter_by(id=answer_id).first()
        if not answer:
            raise NotFoundError(answer_id, "answer")

        if user_logged["id"] != answer.parent_id:
            raise NotAuthorizedError

        data["updated_at"] = dt.now()

        for key, value in data.items():
            setattr(answer, key, value)

        session.add(answer)
        session.commit()

        return jsonify(serialize_answer(answer)), HTTPStatus.OK

    except AttributeError:
        return {"Error": "Answer not found"}, HTTPStatus.NOT_FOUND
    except (
        NotAuthorizedError,
        NotFoundError,
        InvalidKeyError,
        InvalidTypeValueError,
    ) as e:
        return e.message, e.status


@jwt_required()
def delete_answer(answer_id: int):
    user_logged = get_jwt_identity()

    session: Session = db.session
    answer: AnswerModel = session.query(AnswerModel).filter_by(id=answer_id).first()

    try:
        if not answer:
            raise NotFoundError(answer_id, "answer")
        if user_logged["id"] != answer.parent_id:
            raise NotAuthorizedError
        session.delete(answer)
        session.commit()

        return "", HTTPStatus.NO_CONTENT

    except (NotAuthorizedError, NotFoundError) as e:
        return e.message, e.status
