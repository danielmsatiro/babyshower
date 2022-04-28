from http import HTTPStatus
from flask import jsonify, request
from app.configs.database import db
from sqlalchemy.orm import Session, Query
from app.models import ProductModel, CategoryModel
from flask_jwt_extended import jwt_required, get_jwt_identity


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
            
    products: Query = query.offset(page*per_page).limit(per_page).all()

    return {"products": products}, 200


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
        response = query.filter(CategoryModel.name == category).first()
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
