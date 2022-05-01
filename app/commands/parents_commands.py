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
            try:
                parents.append(
                    ParentModel(
                        cpf=fake.ean(length=13)[:11],
                        username=fake.user_name(),
                        name=fake.name(),
                        email=fake.email(),
                        password=fake.ean(length=8),
                        phone=fake.phone_number(),
                        estado=fake.estado_nome(),
                        nome_municipio=fake.city(),
                    )
                )
            except Exception:
                continue

        session.add_all(parents)
        session.commit()

    return parent_group
