from sqlalchemy.orm import Query, Session
from flask import request, current_app, jsonify
from http import HTTPStatus
from flask_jwt_extended import jwt_required, get_jwt_identity
from ipdb import set_trace

from app.configs.database import db
from app.models.answer_model import AnswerModel
from app.models.question_model import QuestionModel
from app.models.product_model import ProductModel


@jwt_required()
def create_answer(product_id: int):
    data = request.get_json()
    user_logged = get_jwt_identity()

    session: Session = db.session

    question: QuestionModel = (
        session.query(QuestionModel).filter_by(id=product_id).first()
    )

    product: ProductModel = (
        session.query(ProductModel).filter_by(id=question.product_id).first()
    )

    if user_logged["id"] != product.parent_id:
        return {"message": "Error"}, HTTPStatus.BAD_REQUEST

    data["parent_id"] = user_logged["id"]
    data["question_id"] = id

    new_answer = AnswerModel(**data)

    session.add(new_answer)
    session.commit()

    set_trace()
    return jsonify(new_answer), HTTPStatus.CREATED


def read_answer(answer_id: int):
    answer = AnswerModel.query.filter_by(id=answer_id).first()

    return jsonify(answer), HTTPStatus.OK


@jwt_required()
def update_answer(answer_id: int):
    data = request.get_json()
    user_logged = get_jwt_identity()

    session: Session = db.session

    answer: AnswerModel = session.query(AnswerModel).filter_by(id=answer_id).first()

    if user_logged["id"] != answer.parent_id:
        return {"message": "Error"}, HTTPStatus.BAD_REQUEST

    for key, value in data.items():
        setattr(answer, key, value)

    session.add(answer)
    session.commit()

    return jsonify(answer), HTTPStatus.OK


@jwt_required()
def delete_answer(answer_id: int):
    user_logged = get_jwt_identity()

    session: Session = db.session

    answer: AnswerModel = session.query(AnswerModel).filter_by(id=answer_id).first()

    if user_logged["id"] != answer.parent_id:
        return {"message": "Error"}, HTTPStatus.BAD_REQUEST

    session.delete(answer)
    session.commit()

    return "", HTTPStatus.NO_CONTENT
