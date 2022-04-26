from http import HTTPStatus
from itertools import product
from flask import jsonify, request
from app.configs.database import db
from sqlalchemy.orm import Session, Query
from app.models import ProductModel
from flask_jwt_extended import jwt_required, get_jwt_identity


def get_all():
    #   QUANDO EXISTIR OUTRAS TABELAS P/ PESQUISAR, APLICAR ESSE CÓDIGO DEMOSTRATIVO
    # session : Session = db.session

    # query: Query = (
    #     session.query(ProductModel.name, Parents.id)
    #     .select_from(ProductModel)
    #     .join(Parents)
    # )

    params = dict(request.args.to_dict().items()) # PEGANDO TODOS OS ARGUMENTOS

    # SEPARANDO OS ARGUMENTOS PARA PAGINAÇÃO
    if "page" in params: 
        page = int(params.pop("page"))
    else: 
        page = 1

    if "per_page" in params: 
        per_page = int(params.pop("per_page")) 
    else: 
        per_page = 1

    # VERIFICANDO EXISTENCIA DE ARGUMENTOS PARA FILTRAGEM
    if params:
        query = ProductModel.query

        for column, value in params.items():
            query = query.filter(getattr(ProductModel, column) == value)

        products = query.all()
    else:
        products = ProductModel.query.all()

    # LOGICA DA PAGINAÇÃO
    products_per_page = [ 
      products[item]
      for item in range(per_page*(page-1), per_page*page)
      if len(products) > item
    ]

    # BÁSICA SERIALIZAÇÃO
    products_serializer = [
        product.__dict__
        for product
        in products_per_page
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


# @jwt_required()
def create_product():
    data: dict = request.get_json()

    product = ProductModel(**data)

    session: Session = db.session

    session.add(product)
    session.commit()

    return jsonify(product), HTTPStatus.CREATED 


# @jwt_required()
def update_product(product_id):
    session: Session = db.session
    data: dict = request.get_json()
    base_query: Query = session.query(ProductModel)

    product: ProductModel = base_query.filter_by(id=product_id).first()

    for key, value in data.items():
        setattr(product, key, value)

    session.add(product)
    session.commit()

    return jsonify(product), HTTPStatus.OK


# @jwt_required()
def delete_product(product_id):
    session: Session = db.session
    base_query: Query = session.query(ProductModel)

    product = base_query.get(product_id)

    session.delete(product)
    session.commit()

    return "", HTTPStatus.NO_CONTENT

