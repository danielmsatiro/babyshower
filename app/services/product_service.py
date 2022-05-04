from dataclasses import asdict

from app.configs.database import db
from app.exceptions import NotFoundError
from app.models.category_model import CategoryModel
from app.models.cities_model import CityModel
from app.models.parent_model import ParentModel
from app.models.product_model import ProductModel
from flask import jsonify, request, url_for
from sqlalchemy.orm import Query, Session


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


def products_per_geolocalization(
    products: ProductModel, page, per_page, localization: CityModel, data: dict
):

    session: Session = db.session

    query_city = session.query(CityModel)
    parents_id = session.query(ParentModel.id)

    try:
        if localization:
            user_city = localization.city
            user_state = localization.state
            if user_state and user_city:
                city_current = (
                    query_city.filter_by(city=user_city)
                    .filter_by(state=user_state)
                    .first()
                )
        if "latitude" and "longitude" in data.keys():
            city_current = (
                query_city.filter_by(latitude=float(data["latitude"]))
                .filter_by(longitude=float(data["longitude"]))
                .first()
            )
        if "state" and "city" in data.keys():
            city_current = (
                query_city.filter(CityModel.city.ilike(f"%{data['city']}%"))
                .filter(CityModel.state.ilike(f"%{data['state']}%"))
                .first()
            )

        if "distance" in data.keys():
            distance = data["distance"]
            cities = city_current.get_cities_within_radius(int(distance))
        else:
            cities = city_current.get_cities_within_radius()

        cities_points_id = [city.point_id for city in cities]

        """ for parent in parents_id:
            parent: ParentModel
            if parent.city_point_id in cities_points_id:
                parents_id = parents_id.filter_by(city_point_id=parent.city_point_id) """

        parents_id = parents_id.filter(ParentModel.city_point_id.in_(cities_points_id))

        # parents_id = [parent.id for parent in parents_id.all()]

        products = products.filter(ProductModel.parent_id.in_(parents_id))
    except Exception:
        products: Query = products.offset(page * per_page).limit(per_page).all()
        return jsonify(products), 200

    return jsonify(products.all()), 200


def verify_product_categories(data):
    received_categories = data["categories"]

    db_categories: CategoryModel = CategoryModel.query.all()

    categories_by_name = []

    for item in db_categories:
        categories_by_name.append(item.name)

    unfinded_categories = []

    for categorie in received_categories:
        if categorie not in categories_by_name:
            unfinded_categories.append(categorie)

    return {"categories": categories_by_name, "unfinded": unfinded_categories}


def data_format(data):
    categories = list(data["categories"])

    for i in range(len(categories)):
        categories[i] = categories[i].lower()

    data["categories"] = categories
