from copy import deepcopy
from http import HTTPStatus

from app.configs.database import db
from app.exceptions.products_exceptions import (
    NonexistentParentProductsError,
    NonexistentProductError,
)
from app.models import CategoryModel, ProductModel, category_product
from app.models.parent_model import ParentModel
from app.services.product_service import products_per_geolocalization
from app.services.email_service import email_new_product
from app.services.product_service import serialize_product
from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from ipdb import set_trace
from sqlalchemy.orm import Query, Session
from ipdb import set_trace
from app.models.cities_model import CityModel


@jwt_required(optional=True)
def get_all():
    # Se o token for fornecido automaticamente é possível obter o id
    # e buscar a cidade e o estado do do usuário para a localização.
    user_logged = get_jwt_identity()
    user_municipio = None
    user_estado = None
    if user_logged:
        session: Session = db.session
        query: Query = session.query(ParentModel)
        user = query.filter_by(id=user_logged["id"]).first()
        user: ParentModel
        user_municipio = user.nome_municipio
        user_estado = user.estado

    params = dict(request.args.to_dict().items())

    data = {}

    try:
        data = request.get_json()  # add filter by categories too
    finally:
        session: Session = db.session
        categories = []

        for name in deepcopy(data.get("categories", [])):
            categories.append(session.query(
                CategoryModel).filter_by(name=name).first())

        query: Query = session.query(ProductModel)

        if categories:
            for category in categories:
                query: Query = query.filter(
                    ProductModel.categories.contains(category))

        min_price = data.get("min_price")
        max_price = data.get("max_price")
        title = data.get("title_product")

        if min_price:
            query: Query = query.filter(
                ProductModel.price >= min_price)
        if max_price:
            query: Query = query.filter(
                ProductModel.price <= max_price)
        if title:
            query: Query = query.filter(
                ProductModel.title.ilike(f"%{title}%"))

        page = int(params.get("page", 1)) - 1
        per_page = int(params.get("per_page", 8))

        return products_per_geolocalization(
            query, page, per_page, user_municipio, user_estado, data)


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
        products = ProductModel.query.filter(
            ProductModel.parent_id == parent_id).all()
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
    user_logged = get_jwt_identity()

    data: dict = request.get_json()
    data["parent_id"] = user_logged["id"]

    query: Query = db.session.query(CategoryModel)

    categories = data.pop("categories")

    product = ProductModel(**data)

    for category in categories:
        response = query.filter(
            CategoryModel.name.ilike(f"%{category}%")).first()
        if response:
            product.categories.append(response)

    parent: ParentModel = ParentModel.query.get(product.parent_id)

    session: Session = db.session
    session.add(product)
    session.commit()

    email_new_product(parent.username, product.title, parent.email)

    product_serialized = serialize_product(product)

    return jsonify(product_serialized), HTTPStatus.CREATED


@jwt_required()
def update_product(product_id: int):
    try:
        user_logged = get_jwt_identity()

        data: dict = request.get_json()

        session: Session = db.session
        product: Query = (
            session.query(ProductModel)
            .select_from(ProductModel)
            .filter(ProductModel.id == product_id)
            .filter(ProductModel.parent_id == user_logged["id"])
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
        user_logged = get_jwt_identity()

        session: Session = db.session
        product: Query = (
            session.query(ProductModel)
            .select_from(ProductModel)
            .filter(ProductModel.id == product_id)
            .filter(ProductModel.parent_id == user_logged["id"])
            .first()
        )

        if not product:
            raise NonexistentProductError

        session.delete(product)
        session.commit()

        return "", HTTPStatus.NO_CONTENT

    except NonexistentProductError as err:
        return err.message, HTTPStatus.NOT_FOUND
