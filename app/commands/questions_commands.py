from copy import deepcopy
import click
import random
from app.configs.database import db
from faker import Faker
from flask.cli import AppGroup
from sqlalchemy.orm.session import Session
from app.models import QuestionModel, ParentModel, ProductModel
from sqlalchemy.orm import Query

def questions_cli():
    fake = Faker("pt_BR")
    question_group = AppGroup("questions", help="Create questions")

    @question_group.command("create")
    @click.argument("quantity")
    def create_questions(quantity):
        session: Session = db.session
        
        query_parent: Query = db.session.query(ParentModel.id).all()
        ids_parents = [response._asdict()["id"] for response in query_parent]

        for _ in range(int(quantity)):
            parent_id = deepcopy(ids_parents[random.randint(1, len(ids_parents) - 1)])

            query_product_by_parent: Query = (
                db.session.query(ProductModel.id)
                .filter(ProductModel.parent_id != parent_id)
                .all()
            )


            ids_product_by_parent = [response._asdict()["id"] for response in query_product_by_parent]

            new_question = QuestionModel(
                    question= fake.sentence(nb_words=10),
                    product_id=deepcopy(ids_product_by_parent[random.randint(1, len(ids_product_by_parent) - 1)]),
                    parent_id=parent_id,
            )
            session.add(new_question)
            session.commit()
        
    
    return question_group
