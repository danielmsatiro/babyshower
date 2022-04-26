from http import HTTPStatus
from flask import jsonify, request
from app.configs.database import db
from sqlalchemy.orm import Session, Query
from app.models import ProductModel



def get_all():
    products = ProductModel.query.all()

    products_serializer = [
        product.__dict__
        for product
        in products
    ]

    [
        product.pop('_sa_instance_state')
        for product
        in products_serializer
    ]

    return {"products": products_serializer}, 200


def get_by_id(product_id: int):
    product = ProductModel.query.get(product_id)

    product_serialize = product.__dict__
    product_serialize.pop('_sa_instance_state')

    return product_serialize, 200


def get_by_parent(parent_id):
    products = ProductModel.query.filter(ProductModel.parent_id==parent_id).all()

    products_serializer = [
        product.__dict__
        for product
        in products
    ]

    [
        product.pop('_sa_instance_state')
        for product
        in products_serializer
    ]

    return {"products": products_serializer}, 200


def get_by_params():
    #   QUANDO EXISTIR OUTRAS TABELAS P/ PESQUISAR, APLICAR ESSE CÓDIGO DEMOSTRATIVO
    # session : Session = db.session

    # query: Query = (
    #     session.query(ProductModel.name, Parents.id)
    #     .select_from(ProductModel)
    #     .join(Parents)
    # )
    query = ProductModel.query
    
    for column, value in request.args.to_dict().items():
        query = query.filter(getattr(ProductModel, column) == value)

    products = query.all()

    products_serializer = [
        product.__dict__
        for product
        in products
    ]

    [
        product.pop('_sa_instance_state')
        for product
        in products_serializer
    ]

    return {"products": products_serializer}, 200


def create_product():
    data = request.get_json()

    product = ProductModel(**data)

    session: Session = db.session

    session.add(product)
    session.commit()

    return jsonify(product), HTTPStatus.CREATED 


def update_product(product_id):
    session: Session = db.session
    base_query: Query = session.query(ProductModel)

    data = request.get_json()
    query = base_query.get(product_id)

    for key, value in data.items():
        setattr(query, key, value)

    session.add(query)
    session.commit()

    return jsonify(query), HTTPStatus.OK


def delete_product(product_id):
    session: Session = db.session

    base_query: Query = session.query(ProductModel)
    query = base_query.get(product_id)

    session.delete(query)
    session.commit()

    return "", HTTPStatus.NO_CONTENT

