from http import HTTPStatus
from flask import jsonify
from app.configs.database import db
from sqlalchemy.orm import Query
from app.models.category_model import CategoryModel


def retrieve():
    response: Query = db.session.query(CategoryModel)
    response = response.all()
    return {"categories": response}, HTTPStatus.OK
