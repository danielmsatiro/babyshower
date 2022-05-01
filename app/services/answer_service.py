from dataclasses import asdict
from flask import url_for
from app.models import AnswerModel, ParentModel, ProductModel, QuestionModel
from sqlalchemy.orm import Query, Session
from app.configs.database import db


def serialize_answer(answer: AnswerModel) -> dict:
    answer_serialized = asdict(answer)
    print(f"{answer_serialized=}")

    username = (
        db.session.query(ParentModel.username)
        .select_from(ParentModel)
        .join(QuestionModel)
        .filter(QuestionModel.id == answer_serialized["question_id"])
        .first()
    )

    session: Session = db.session
    parent: Query = (
        session.query(ParentModel.username, QuestionModel.question)
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
                product_id=answer_serialized["question_id"],
            ),
            "question": parent[0],
            "username": username[0],
        }
    }

    answer_serialized.update(url)
    answer_serialized.pop("question_id")

    return answer_serialized
