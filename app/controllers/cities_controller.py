from http import HTTPStatus
from flask import jsonify, request
from app.configs.database import db
from sqlalchemy.orm import Query, Session
from app.models.cities_model import CityModel


def retrieve():
    session: Session = db.session
    response: Query = session.query(CityModel)
    params = dict(request.args.to_dict().items())
    page = int(params.get("page", 1)) - 1
    per_page = int(params.get("per_page", 8))
    response = response.offset(
            page * per_page).limit(per_page).all()
    return {"cities": response}, HTTPStatus.OK
