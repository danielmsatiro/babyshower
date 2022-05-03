from ipdb import set_trace
from dataclasses import asdict

from flask import jsonify, request, url_for
from app.models.cities_model import CityModel
from app.models.parent_model import ParentModel

from app.models.product_model import ProductModel
from sqlalchemy.orm import Query, Session
from app.configs.database import db


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
        product_serialized[
            "categories"][i] = product_serialized["categories"][i][
            "name"
        ]

    return product_serialized


def products_per_geolocalization(
        products: ProductModel,
        page, per_page, localization: CityModel, data: dict):

    session: Session = db.session

    # set_trace()

    query_city = session.query(CityModel)
    parents_id = session.query(ParentModel)

    try:
        if localization:
            user_city = localization.city
            user_state = localization.state
            if user_state and user_city:
                city_current = query_city.filter_by(
                    city=user_city).filter_by(
                        state=user_state).first()
        # set_trace()
        if "latitude" and "longitude" in data.keys():
            city_current = query_city.filter_by(
                latitude=float(data["latitude"])).filter_by(
                    longitude=float(data["longitude"])).first()
        # set_trace()
        if "state" and "city" in data.keys():
            city_current = query_city.filter_by(
                city=data["city"]).filter_by(
                    state=data["state"]).first()
        if "distance" in data.keys():
            distance = data["distance"]
            cities = city_current.get_cities_within_radius(int(distance))
        else:
            cities = city_current.get_cities_within_radius()

        cities_points_id = [city.point_id for city in cities]
        # set_trace()
        for parent in parents_id:
            parent: ParentModel
            if parent.city_point_id in cities_points_id:
                parents_id = parents_id.filter_by(
                        city_point_id=parent.city_point_id)

        parents_id = [parent.id for parent in parents_id.all()]

        products_parent_id = [product.parent_id for product in products.all()]
        # set_trace()
        # for parent_id in parents_id:
        #     if parent_id in products_parent_id:
        # set_trace()
        products = products.filter(ProductModel.parent_id.in_(parents_id))
        # set_trace()
        # print(products)
        # products = products.offset(page * per_page).limit(per_page).all()
        # set_trace()
    except Exception:
        print("cheguei")
        products: Query = products.offset(
            page * per_page).limit(per_page).all()
        return jsonify(products), 200

    return jsonify(products.all()), 200
