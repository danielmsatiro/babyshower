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

def read_answer(id):
    answer = (
        AnswerModel
        .query
        .filter_by(id=id)
        .first()
    )

    return jsonify(answer), HTTPStatus.OK

def update_answer(id):
    data = request.get_json()

    session = current_app.db.session

    answer = AnswerModel.query.get(id)

    for key, value in data.items():
        setattr(answer, key, value)

    session.add(answer)
    session.commit()

    return jsonify(answer), HTTPStatus.OK

def delete_answer(id):
    session = current_app.db.session

    answer = AnswerModel.query.get(id)

    session.delete(answer)
    session.commit()

    return "", HTTPStatus.NO_CONTENT
    