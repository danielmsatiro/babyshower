from app.configs.database import db
from app.models import AnswerModel, QuestionModel
from faker import Faker
from flask.cli import AppGroup


def answers_cli():
    fake = Faker("pt_BR")
    answer_group = AppGroup("answers", help="Create answers")

    @answer_group.command("create")
    def create_answers():

        questions = db.session.query(QuestionModel).all()

        if not questions:
            raise Warning("Falta incluir perguntas")

        for question in questions:
            new_answer = AnswerModel(
                answer=fake.sentence(nb_words=10),
                question_id=question.id,
                parent_id=question.parent_id,
            )
            db.session.add(new_answer)
            db.session.commit()
        print(f"answers added for each question ({len(questions)} questions)")

    return answer_group
