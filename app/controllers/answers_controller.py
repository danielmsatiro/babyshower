import sqlalchemy
from flask import request, current_app, jsonify
from http import HTTPStatus

from app.models.answer_model import AnswerModel


def create_answer(id):
    data = request.get_json()

    data["question_id"] = id

    session = current_app.db.session

    new_answer = AnswerModel(**data)

    session.add(new_answer)
    session.commit()

    return jsonify(new_answer), HTTPStatus.CREATED

