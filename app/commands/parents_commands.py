import random
import click
from app.configs.database import db
from app.models.parent_model import ParentModel
from faker import Faker
from flask.cli import AppGroup
from sqlalchemy.orm.session import Session


def parents_cli():
    fake: Faker = Faker("pt_BR")
    parent_group = AppGroup("parents", help="Create parents")

    @parent_group.command("create")
    @click.argument("quantity")
    def create_parents(quantity):
        session: Session = db.session
        parents = []

        for _ in range(int(quantity)):
            number = fake.msisdn()
            phone_number = f"({number[2:4]}) {number[4:9]}-{8348}"
            try:
                parents.append(
                    ParentModel(
                        cpf=fake.ean(length=13)[:11],
                        username=fake.user_name(),
                        name=fake.name(),
                        email=fake.email(),
                        password=fake.ean(length=8),
                        phone=phone_number,
                        city_point_id=random.randint(1, 10 - 1),
                    )
                )
            except Exception:
                print("print")
                continue

        session.add_all(parents)
        session.commit()

        print(f"{quantity} parents added")

    return parent_group
