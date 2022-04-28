import random
from copy import deepcopy

import click
from app.configs.database import db
from app.models import ParentModel, ProductModel
from flask.cli import AppGroup
from sqlalchemy.orm import Query
from sqlalchemy.orm.session import Session


def products_cli():
    product_group = AppGroup("products", help="Create products")

    products_names_list = [
        "Bebê conforto para bebês de 3 meses",
        "Bebê conforto para bebês de 6 meses",
        "Bebê conforto para bebês de 9 meses",
        "Bebê conforto para bebês de 1 ano",
        "Bebê conforto para bebês de 2 anos",
        "Bebê conforto para crianças de 3 a 5 anos",
        "carrinhos",
        "roupas",
        "acessórios",
        "mamães",
        "roupa de banho para bebê",
        "brinquedos",
        "lactação",
        "segurança",
        "saúde",
    ]

    @product_group.command("create")
    @click.argument("quantity")
    def create_products(quantity):
        session: Session = db.session

        query: Query = db.session.query(ParentModel.id).all()
        ids_parents = [response._asdict()["id"] for response in query]

        for _ in range(int(quantity)):
            radom_title = random.randint(0, 14)
            random_price = round(random.uniform(5.0, 1000.0), 2)
            random_id = deepcopy(ids_parents[random.randint(1, len(ids_parents) - 1)])

            products = ProductModel(
                title=products_names_list[radom_title],
                price=random_price,
                parent_id=random_id,
                description="Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book.",
                image="https://imagem/320x240",
            )
            session.add(products)
            session.commit()

        # session.add_all(products)

    return product_group
