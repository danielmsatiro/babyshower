import random
from copy import deepcopy

from app.commands.products_list import products_list
from app.configs.database import db
from app.models import CategoryModel, CityModel, ParentModel, ProductModel
from app.services.add_categories import add_categories_if_empty
from faker import Faker
from flask.cli import AppGroup
from sqlalchemy.orm import Session


def total_cli():
    fake: Faker = Faker("pt_BR")
    total_group = AppGroup("populate", help="Populate Brazil")

    @total_group.command("brazil")
    def populate_brazil():
        session: Session = db.session
        cities = session.query(CityModel.point_id).all()
        add_categories_if_empty()
        products = []

        for point in cities:
            try:
                # One parent for each city
                parent = ParentModel(
                    cpf=fake.ean(length=13)[:11],
                    username=f"{fake.user_name()}{point[0]}",
                    name=fake.name(),
                    email=f"{point[0]}{'teste@gmail.com'}",
                    password=fake.ean(length=8),
                    phone=f"(21) 99999-9999",
                    city_point_id=point[0],
                )  
                session.add(parent)
                session.commit()
                # One product for each parent
                random_product = random.randint(0, len(products_list) - 1)

                data = deepcopy(products_list[random_product])
                categories = data.pop("categories")

                product = ProductModel(
                    title=products_list[random_product]["title"],
                    price=products_list[random_product]["price"],
                    parent_id=parent.id,
                    description=fake.sentence(nb_words=20),
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

                products.append(product)
            except Exception:
                print(f"error generating in city")
        try:
            session.add_all(products)
            session.commit()
        except Exception:
            print(f"error generating in products")

            # Two questions for each product from others parents

        print(f"{len(cities)} parents added for city with one product")

    return total_group
