import random
from copy import deepcopy

import click
from app.configs.database import db
from app.models import CategoryModel, ParentModel, ProductModel
from flask.cli import AppGroup
from ipdb import set_trace
from sqlalchemy.orm import Query
from sqlalchemy.orm.session import Session


def products_cli():
    product_group = AppGroup("products", help="Create products")

    products_list = [
        {"title": "tiptop", "price": 35.60, "categories": ["0 a 3 meses", "roupas"]},
        {
            "title": "carrinho de bebê novinho",
            "price": 650.00,
            "categories": [
                "carrinhos",
                "0 a 3 meses",
                "4 a 6 meses",
                "7 a 9 meses",
                "10 meses a 1 ano",
                "2 anos",
                "3 a 5 anos",
            ],
        },
        {
            "title": "body tamanho p",
            "price": 29.90,
            "categories": ["0 a 3 meses", "roupas"],
        },
        {
            "title": "carrinho de bebê",
            "price": 569.00,
            "categories": [
                "carrinhos",
                "0 a 3 meses",
                "4 a 6 meses",
                "7 a 9 meses",
                "10 meses a 1 ano",
                "2 anos",
                "3 a 5 anos",
            ],
        },
        {
            "title": "poltrona de amamentação reclinável",
            "price": 759.00,
            "categories": ["lactação", "quarto do bebê"],
        },
        {
            "title": "babá eletrônica",
            "price": 250.00,
            "categories": [
                "segurança para bebê",
                "0 a 3 meses",
                "4 a 6 meses",
                "7 a 9 meses",
                "10 meses a 1 ano",
                "2 anos",
                "3 a 5 anos",
            ],
        },
        {
            "title": "berço",
            "price": 560.00,
            "categories": [
                "quarto do bebê",
                "0 a 3 meses",
                "4 a 6 meses",
                "7 a 9 meses",
                "10 meses a 1 ano",
                "2 anos",
                "3 a 5 anos",
            ],
        },
        {"title": "cobertorzinho", "price": 45.00, "categories": []},
        {"title": "Nanina", "price": 15.00, "categories": ["brinquedos"]},
        {"title": "body tamanho M", "price": 36.00, "categories": ["roupas"]},
        {
            "title": "Tênis tam 16",
            "price": 36.00,
            "categories": ["roupas", "0 a 3 meses"],
        },
        {
            "title": "jardineira",
            "price": 49.90,
            "categories": ["roupas", "4 a 6 meses"],
        },
        {
            "title": "colchão para carrinho de bebê",
            "price": 20.00,
            "categories": ["quarto do bebê"],
        },
        {
            "title": "bebê-conforto",
            "price": 350.00,
            "categories": [
                "segurança para bebê",
                "0 a 3 meses",
                "4 a 6 meses",
                "7 a 9 meses",
                "10 meses a 1 ano",
                "2 anos",
            ],
        },
    ]

    @product_group.command("create")
    @click.argument("quantity")
    def create_products(quantity):
        session: Session = db.session

        query: Query = db.session.query(ParentModel.id).all()

        ids_parents = [response._asdict()["id"] for response in query]

        for _ in range(int(quantity)):
            random_product = random.randint(0, len(products_list) - 1)
            random_id = deepcopy(ids_parents[random.randint(1, len(ids_parents) - 1)])

            data = deepcopy(products_list[random_product])
            categories = data.pop("categories")

            product = ProductModel(
                title=products_list[random_product]["title"],
                price=products_list[random_product]["price"],
                parent_id=random_id,
                description="Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book.",
                image="https://imagem/320x240",
            )

            for category in categories:

                response = (
                    session.query(CategoryModel)
                    .filter(CategoryModel.name.ilike(f"%{category}%"))
                    .first()
                )

                if response:
                    product.categories.append(response)

            session.add(product)
            session.commit()

    return product_group
