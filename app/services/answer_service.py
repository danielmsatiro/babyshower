from dataclasses import asdict

from app.configs.database import db
from app.models import AnswerModel, ParentModel, ProductModel, QuestionModel
from flask import url_for
from sqlalchemy.orm import Query, Session


def serialize_answer(answer: AnswerModel) -> dict:
    answer_serialized = asdict(answer)

    username = (
        db.session.query(ParentModel.username)
        .select_from(ParentModel)
        .join(QuestionModel)
        .filter(QuestionModel.id == answer_serialized["question_id"])
        .first()
    )

    session: Session = db.session
    parent: Query = (
        session.query(ParentModel.username, QuestionModel.question, ProductModel.id)
        .select_from(ParentModel)
        .join(ProductModel)
        .filter(ParentModel.id == ProductModel.parent_id)
        .join(QuestionModel)
        .filter(ProductModel.id == QuestionModel.product_id)
        .filter(QuestionModel.id == answer_serialized["question_id"])
        .first()
    )

    url = {
        "question": {
            "link": url_for(
                "bp_api.bp_questions.get_product_questions",
                product_id=parent[2],
            ),
            "question": parent[1],
            "username": username[0],
        }
    }

    answer_serialized.update(url)
    answer_serialized.pop("question_id")

    return answer_serialized
