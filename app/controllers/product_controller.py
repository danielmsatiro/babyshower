from flask import request
from app.models import ProductModel

# from app.configs.database import db # ACOMPANHA O CÓDIGO COMENTADO ABAIXO
# from sqlalchemy.orm import Session, Query


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

