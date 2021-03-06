from copy import deepcopy
from http import HTTPStatus

from app.configs.database import db
from app.exceptions import InvalidKeyError, NotFoundError
from app.exceptions.categories_exc import InvalidCategoryError
from app.exceptions.products_exceptions import InvalidTypeNumberError
from app.models import CategoryModel, ProductModel
from app.models.cities_model import CityModel
from app.models.parent_model import ParentModel
from app.services.add_categories import add_categories_if_empty
from app.services.email_service import email_new_product
from app.services.product_service import (
    data_format,
    find_category,
    products_per_geolocalization,
    serialize_product,
    verify_product_categories,
)
from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy.orm import Query, Session


@jwt_required(optional=True)
def get_all():
    user_logged = get_jwt_identity()
    localization = None
    if user_logged:
        session: Session = db.session
        parents: Query = session.query(ParentModel)
        cities: Query = session.query(CityModel)
        user: ParentModel = parents.filter_by(id=user_logged["id"]).first()
        localization: CityModel = cities.filter_by(point_id=user.city_point_id).first()

    params = dict(request.args.to_dict().items())

    data = {}

    try:
        data = request.get_json()  # add filter by categories too
    finally:
        session: Session = db.session
        categories = []

        for name in deepcopy(data.get("categories", [])):
            categories.append(session.query(CategoryModel).filter_by(name=name).first())

        query: Query = session.query(ProductModel)

        if categories:
            for category in categories:
                query: Query = query.filter(ProductModel.categories.contains(category))

        min_price = data.get("min_price")
        max_price = data.get("max_price")
        title = data.get("title_product")

        if min_price:
            query: Query = query.filter(ProductModel.price >= min_price)
        if max_price:
            query: Query = query.filter(ProductModel.price <= max_price)
        if title:
            query: Query = query.filter(ProductModel.title.ilike(f"%{title}%"))

        page = int(params.get("page", 1)) - 1
        per_page = int(params.get("per_page", 8))
        return products_per_geolocalization(query, page, per_page, localization, data)


def get_by_id(product_id: int):
    try:
        session: Session = db.session
        product = (
            session.query(ProductModel).filter(ProductModel.id == product_id).first()
        )
        product_serialized = serialize_product(product)

        if not product:
            raise NotFoundError(product_id, "product")

        return jsonify(product_serialized), HTTPStatus.OK

    except NotFoundError as e:
        return e.message, e.status


def get_by_parent(parent_id: int):
    try:
        session: Session = db.session
        products = (
            session.query(ProductModel)
            .filter(ProductModel.parent_id == parent_id)
            .all()
        )

        if not products:
            raise NotFoundError(parent_id, "parent")

        for i in range(len(products)):
            product_serialized = serialize_product(products[i])
            products[i] = product_serialized

        return {"products": products}, HTTPStatus.OK

    except NotFoundError as e:
        return e.message, e.status


@jwt_required()
def create_product():
    add_categories_if_empty()
    try:
        user_logged = get_jwt_identity()

        data: dict = request.get_json()
        received_key = set(data.keys())

        available_keys = {
            "title",
            "description",
            "price",
            "image1",
            "image2",
            "image3",
            "image4",
            "categories",
        }

        data_format(data)

        verified = verify_product_categories(data)

        if len(verified["unfinded"]) > 0:
            raise InvalidCategoryError(verified["unfinded"])

        if not received_key == available_keys:
            raise InvalidKeyError(received_key, available_keys)

        data["parent_id"] = user_logged["id"]

        query: Query = db.session.query(CategoryModel)

        categories = data.pop("categories")

        product = ProductModel(**data)

        for category in categories:
            response = query.filter(CategoryModel.name.ilike(f"%{category}%")).first()
            if response:
                product.categories.append(response)

        parent: ParentModel = ParentModel.query.get(product.parent_id)

        session: Session = db.session
        session.add(product)
        session.commit()

        # email_new_product(parent.username, product.title, parent.email)
        product_serialized = serialize_product(product)

        return jsonify(product_serialized), HTTPStatus.CREATED

    except (InvalidTypeNumberError, InvalidKeyError, InvalidCategoryError) as e:
        return e.message, e.status


@jwt_required()
def update_product(product_id: int):
    data: dict = request.get_json()

    available_keys = {
        "title",
        "price",
        "description",
        "image1",
        "image2",
        "image3",
        "image4",
        "categories",
    }

    received_keys = set(data.keys())

    data_format(data)

    user_logged = get_jwt_identity()

    try:

        if not received_keys.issubset(available_keys):
            raise InvalidKeyError(received_keys, available_keys)

        if "categories" in data:
            received_categories = data.pop("categories")
            find_categories = [
                find_category(category) for category in received_categories
            ]
            data["categories"] = find_categories

        session: Session = db.session
        product: Query = (
            session.query(ProductModel)
            .select_from(ProductModel)
            .filter(ProductModel.id == product_id)
            .filter(ProductModel.parent_id == user_logged["id"])
            .first()
        )

        if not product:
            raise NotFoundError(product_id, "product")

        for key, value in data.items():
            setattr(product, key, value)

        session.add(product)
        session.commit()

        product_serialized = serialize_product(product)

        return jsonify(product_serialized), HTTPStatus.OK

    except (NotFoundError, InvalidCategoryError) as e:
        return e.message, e.status


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
            raise NotFoundError(product_id, "product")

        session.delete(product)
        session.commit()

        return "", HTTPStatus.NO_CONTENT

    except NotFoundError as e:
        return e.message, e.status
