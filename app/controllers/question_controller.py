from http import HTTPStatus

from app.configs.database import db
from app.models import QuestionModel
from flask import jsonify, request, session
from flask_jwt_extended import jwt_required
from sqlalchemy.orm import Query, Session


def get_product_questions(product_id: int):

    return {"msg": "Rota GET perguntas do produto"}
    

# @jwt_required()
def create_question(product_id: int):
    data: dict = request.get_json()

    data["product_id"] = product_id

    question = QuestionModel(**data)

    session: Session = db.session
    session.add(question)
    session.commit

    return jsonify(question), HTTPStatus.CREATED


# @jwt_required()
def update_question(question_id: int):
    data: dict = request.get_json()
    
    session: Session = db.session

    question = session.query(QuestionModel).get(question_id)

    for key, value in data.items():
        setattr(question, key, value)
    
    session.commit()

    return jsonify(question), HTTPStatus.OK


# @jwt_required()
def delete_question(question_id: int):
    session: Session = db.session

    question = session.query(QuestionModel).get(question_id)

    session.delete(question)
    session.commit()

    return "", HTTPStatus.NO_CONTENT
