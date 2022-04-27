import click
from app.configs.database import db
from app.models.question_model import QuestionModel
from faker import Faker
from flask.cli import AppGroup
from sqlalchemy.orm.session import Session

def questions_cli():
    fake = Faker("pt_BR")
    question_group = AppGroup("questions", help="Create questions")

    @question_group.command("create")
    @click.argument("quantity")
    def create_questions(quantity):
        session: Session = db.session
        questions = []

        for i in range(int(quantity)):
            try:
                questions.append(
                    QuestionModel(
                        question= fake.sentence(nb_words=10),
                        product_id=1,
                        parent_id=1,
                    )
                )
            except:
                continue
        
        session.add_all(questions)
        session.commit()
    
    return question_group
