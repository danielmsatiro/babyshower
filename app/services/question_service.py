from dataclasses import asdict
from flask import url_for
from app.models import AnswerModel, ParentModel, ProductModel, QuestionModel
from sqlalchemy.orm import Query, Session
from app.configs.database import db


def serialize_answer(question: QuestionModel) -> dict:
    question_serialized = asdict(question)
    print("="*80)
    print(question)
    print("="*80)

    session: Session = db.session

    username = (db.session
        .query(ParentModel.username)
        .select_from(ParentModel)
        .join(QuestionModel)
        .filter(ParentModel.id == QuestionModel.parent_id)
        .first()
    )
    
    if question.answer:
        query: Query = session.query(AnswerModel.id, AnswerModel.answer, ParentModel.username)
    else:
        query: Query = session.query(ParentModel.username)

    query: Query = (
        query.select_from(ParentModel)
        .join(ProductModel)
        .filter(ParentModel.id == ProductModel.parent_id)
        .join(QuestionModel)
        .filter(ProductModel.id == question_serialized["product_id"])
    )
    if question.answer:
        query: Query = (
            query.join(AnswerModel)
                .filter(AnswerModel.question_id == QuestionModel.id)
                .filter(QuestionModel.id == question_serialized["answer"]["question_id"])
        )
    result = query.first()
    print(query)

    if question.answer:
        answer = {
            "username": username[0],
            "answer": {
                "link": url_for('bp_api.bp_answers.read_answer', answer_id=result[0]),
                "username": result[2],
                "answer": result[1]

            }
        }
    else:
        answer = {
            "username": username[0],
            "answer": "A responder"
        }
    
    question_serialized.update(answer)
    print(question_serialized)
    # question_serialized.pop('question_id')
    
    return question_serialized
