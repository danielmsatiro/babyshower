from dataclasses import asdict

from flask import url_for

from app.models.product_model import ProductModel


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

    return product_serialized
