from http import HTTPStatus

from app.configs.database import db
from app.models import CategoryModel, ProductModel, ParentModel
from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy.orm import Query, Session
from ipdb import set_trace
from app.models.cities_model import CityModel


def get_all():
    params = dict(request.args.to_dict().items())
    session: Session = db.session

    if "page" in params:
        page = int(params.pop("page")) - 1
    else:
        page = 0

    if "per_page" in params:
        per_page = int(params.pop("per_page"))
    else:
        per_page = 8

    query = ProductModel.query
    teste = session.query(ProductModel).all()
    query_city = session.query(CityModel)
    parents = session.query(ParentModel)

    for key, value in params.items():
        if "price" in key:
            print("entrou aqui")
            query: Query = query.filter(ProductModel.price <= value)
        elif "title" in key:
            query: Query = query.filter(ProductModel.title in key)

    # get all products
    #     products: Query = query.offset(page * per_page).limit(per_page).all()
    #     products: Query = query.filter_by(parent_id=1).all()
    #     products: Query = query

    distance = params.get("distance")
    city_current = query_city.filter_by(nome_municipio='Abadia de Goiás').first()
    cities = city_current.get_cities_within_radius(int(distance))


    # pegar produtos por varios estados a partir da distancia
    products_lista = []
    for city in cities:
        city: CityModel
        for product in teste:
            product_onwer = parents.filter_by(id=product.parent_id).first()
            product_onwer: ProductModel
            if (
                city.nome_municipio == product_onwer.nome_municipio
                and product not in products_lista
            ):
                products_lista.append(product)
    return jsonify(products_lista), 200


def get_by_id(product_id: int):
    product = ProductModel.query.get(product_id)
    return jsonify(product), 200


def get_by_parent(parent_id):
    products = ProductModel.query.filter(ProductModel.parent_id == parent_id).first()
    return {"products": products}, 200


@jwt_required()
def create_product():
    parent = get_jwt_identity()

    data: dict = request.get_json()
    data["parent_id"] = parent["id"]

    query: Query = db.session.query(CategoryModel)

    categories = data.pop("categories")

    product = ProductModel(**data)

    for category in categories:
        response = query.filter(CategoryModel.name.ilike(f"%{category}%")).first()
        if response:
            product.categories.append(response)

    session: Session = db.session
    session.add(product)
    session.commit()

    return jsonify(product), HTTPStatus.CREATED


@jwt_required()
def update_product(product_id):
    parent = get_jwt_identity()

    session: Session = db.session
    data: dict = request.get_json()

    product: Query = (
        session.query(ProductModel)
        .select_from(ProductModel)
        .filter(ProductModel.id == product_id)
        .filter(ProductModel.parent_id == parent["id"])
        .first()
    )

    if not product:
        return {"Error": "UNAUTHORIZED"}, HTTPStatus.UNAUTHORIZED

    for key, value in data.items():
        setattr(product, key, value)

    session.add(product)
    session.commit()

    return jsonify(product), HTTPStatus.OK


@jwt_required()
def delete_product(product_id):
    parent = get_jwt_identity()

    session: Session = db.session

    product: Query = (
        session.query(ProductModel)
        .select_from(ProductModel)
        .filter(ProductModel.id == product_id)
        .filter(ProductModel.parent_id == parent["id"])
        .first()
    )

    if not product:
        return {"Error": "UNAUTHORIZED"}, HTTPStatus.UNAUTHORIZED

    session.delete(product)
    session.commit()

    return "", HTTPStatus.NO_CONTENT
