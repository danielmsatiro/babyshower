from http import HTTPStatus

from app.configs.database import db
from app.models import CategoryModel, ProductModel
from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy.orm import Query, Session

from app.services.product_service import serialize_product


def get_all():
    params = dict(request.args.to_dict().items())

    if "page" in params:
        page = int(params.pop("page")) - 1
    else:
        page = 0

    if "per_page" in params:
        per_page = int(params.pop("per_page"))
    else:
        per_page = 8

    query = ProductModel.query

    for column, value in params.items():
        if "price" in column:
            print("entrou aqui")
            query: Query = query.filter(ProductModel.price <= value)
        elif "title" in column:
            query: Query = query.filter(ProductModel.title in column)

    products: Query = query.offset(page * per_page).limit(per_page).all()

    for i in range(len(products)):
        product_serialized = serialize_product(products[i])
        products[i] = product_serialized

    return {"products": products}, 200


def get_by_id(product_id: int):
    product = ProductModel.query.get(product_id)
    product_serialized = serialize_product(product)

    return jsonify(product_serialized), 200


def get_by_parent(parent_id):
    products = ProductModel.query.filter(ProductModel.parent_id == parent_id).all()

    for i in range(len(products)):
        product_serialized = serialize_product(products[i])
        products[i] = product_serialized
    
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
    
    product_serialized = serialize_product(product)

    return jsonify(product_serialized), HTTPStatus.CREATED


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

    product_serialized = serialize_product(product)

    return jsonify(product_serialized), HTTPStatus.OK


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
