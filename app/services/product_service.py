from dataclasses import asdict

from app.models.product_model import ProductModel
from app.models.category_model import CategoryModel
from flask import url_for

from app.exceptions import NotFoundError


def serialize_product(product: ProductModel) -> dict:
    product_serialized = asdict(product)
    url = {
        "questions": url_for(
            "bp_api.bp_questions.get_product_questions",
            product_id=product_serialized["id"],
        )
    }
    product_serialized.update(url)

    for i in range(len(product_serialized["categories"])):
        product_serialized["categories"][i] = product_serialized["categories"][i][
            "name"
        ]

    product_serialized["price"] = float(product_serialized["price"])

    return product_serialized


def verify_product_categories(data):
    received_categories = data["categories"]

    db_categories: CategoryModel = (
        CategoryModel
        .query
        .all()
    )

    categories_by_name = []

    for item in db_categories:
        categories_by_name.append(item.name)

    unfinded_categories = []

    for categorie in received_categories:
        if categorie not in categories_by_name:
            unfinded_categories.append(categorie)

    return {
        "categories": categories_by_name,
        "unfinded": unfinded_categories
    }


def data_format(data):
    categories = list(data["categories"])

    print(categories)

    for i in range(len(categories)):
        categories[i] = categories[i].lower()

    data["categories"] = categories
        