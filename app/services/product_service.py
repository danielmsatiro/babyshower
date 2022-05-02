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

    query_city = session.query(CityModel)
    parents = session.query(ParentModel)

    products_list = []

    try:
        if localization:
            user_city = localization.city
            user_state = localization.state
            if user_state and user_city:
                city_current = query_city.filter_by(
                    city=user_city).filter_by(
                        state=user_state).first()
        if "latitude" and "longitude" in data.keys():
            city_current = query_city.filter_by(
                latitude=float(data["latitude"])).filter_by(
                    longitude=float(data["longitude"])).first()
        if "state" and "city" in data.keys():
            city_current = query_city.filter_by(
                city=data["city"]).filter_by(
                    state=data["state"]).first()
        if "distance" in data.keys():
            distance = data["distance"]
            cities = city_current.get_cities_within_radius(int(distance))
        else:
            cities = city_current.get_cities_within_radius()

        # parents_id = session.query(ParentModel.id).filter_by(city_id==point_id).all() 
        parents_id: Query = session.query(ParentModel.id).all()

        print(parents_id)

        return ""

        # for city in cities:
        #     city: CityModel
        #     for product in products:
        #         product_onwer = parents.filter_by(id=product.parent_id).first()
        #         product_onwer: ProductModel
        #         if (
        #             city.nome_municipio == product_onwer.nome_municipio
        #             and product not in products_list
        #         ):
        #             products_list.append(product)
        # if (page or page == 0) and per_page:
        #     if page == 0:
        #         page = 1
        #     date_response = {"products": []}
        #     products_limit = page * per_page
        #     if products_limit > len(products_list):
        #         products_limit = len(products_list)
        #     for x in range(products_limit-products_limit, products_limit):
        #         print("passei do for")
        #         date_response["products"].append(products_list[x])
        #     return date_response, 200

    except Exception:
        products: Query = products.offset(
            page * per_page).limit(per_page).all()
        return jsonify(products), 200

    return jsonify(products_list), 200
