from http import HTTPStatus

from app.configs.database import db
from app.models.category_model import CategoryModel
from sqlalchemy.orm import Query


def retrieve():
    response: Query = db.session.query(CategoryModel)
    response = response.all()
    return {"categories": response}, HTTPStatus.OK
