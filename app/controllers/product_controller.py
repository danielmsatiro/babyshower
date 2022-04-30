from http import HTTPStatus

from app.configs.database import db
from app.exceptions.products_exceptions import (
    NonexistentParentProductsError,
    NonexistentProductError,
)
from app.models import CategoryModel, ProductModel
from app.services.product_service import serialize_product
from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from ipdb import set_trace
from sqlalchemy.orm import Query, Session


def get_all():
    params = dict(request.args.to_dict().items())
    data = None
    try:
        data: dict = request.get_json()  # add filter by categories too
    finally:
        # set_trace()

        if "page" in params:
            page = int(params.pop("page")) - 1
        else:
            page = 0

        if "per_page" in params:
            per_page = int(params.pop("per_page"))
        else:
            per_page = 8

        query = ProductModel.query

        for key, value in params.items():
            if "min_price" == key.lower():
                query: Query = query.filter(ProductModel.price >= value)
            if "max_price" == key.lower():
                query: Query = query.filter(ProductModel.price <= value)
            elif "title" == key.lower():
                query: Query = query.filter(ProductModel.title.ilike(f"%{value}%"))

        products: Query = query.offset(page * per_page).limit(per_page).all()

        for i in range(len(products)):
            product_serialized = serialize_product(products[i])
            products[i] = product_serialized

        return {"products": products}, HTTPStatus.OK


def get_by_id(product_id: int):
    try:
        product = ProductModel.query.get(product_id)
        product_serialized = serialize_product(product)

        if not product:
            raise NonexistentProductError

        return jsonify(product_serialized), HTTPStatus.OK

    except NonexistentProductError as err:
        return err.message, HTTPStatus.NOT_FOUND


def get_by_parent(parent_id: int):
    try:
        products = ProductModel.query.filter(ProductModel.parent_id == parent_id).all()
        if not products:
            raise NonexistentParentProductsError

        for i in range(len(products)):
            product_serialized = serialize_product(products[i])
            products[i] = product_serialized

        return {"products": products}, HTTPStatus.OK

    except NonexistentParentProductsError as err:
        return err.message, HTTPStatus.NOT_FOUND


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
def update_product(product_id: int):
    try:
        parent = get_jwt_identity()

        data: dict = request.get_json()

        session: Session = db.session
        product: Query = (
            session.query(ProductModel)
            .select_from(ProductModel)
            .filter(ProductModel.id == product_id)
            .filter(ProductModel.parent_id == parent["id"])
            .first()
        )

        if not product:
            raise NonexistentProductError

        for key, value in data.items():
            setattr(product, key, value)

        session.add(product)
        session.commit()

        product_serialized = serialize_product(product)

        return jsonify(product_serialized), HTTPStatus.OK

    except NonexistentProductError as err:
        return err.message, HTTPStatus.NOT_FOUND


@jwt_required()
def delete_product(product_id: int):
    try:
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
            raise NonexistentProductError

        session.delete(product)
        session.commit()

        return "", HTTPStatus.NO_CONTENT

    except NonexistentProductError as err:
        return err.message, HTTPStatus.NOT_FOUND
